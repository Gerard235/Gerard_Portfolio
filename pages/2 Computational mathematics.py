import streamlit as st
import sys
sys.path.append("./gerard_portfolio")
from PIL import Image
from captcha1 import captcha_control

captcha_control()


def Comp_Math_page():
    st.title("Gerard's web portfolio")

    with st.expander("Fitting a polynomial to data using the singular value decomposition"):
        st.markdown(r'''
                    When analysing data, often a good starting point is to fit a polynomial of degree $n$ to those data. In this exercise, I demonstrate how we can approach this problem with linear algebra, in particular the singular value decomposition (SVD) of a matrix representing input data provides an algorithm to find the polynomial that fits the data. The SVD also helps with reducing overfitting and improving numerical stability.

                    To illustrate this our data will be 
                    $$
                    \begin{align}
                    t, \hat{f}(t)
                    \end{align}
                    $$ 
                    where $t$ will be $m$ equally spaced points along the unit interval (i.e., $t=t_1, \cdots, t_m$), the function $\hat{f}$ wil be equal to $f(t) = 2 + \cos(8t) + \sin(16t)$ plus a random perturbation. 

                    To fit an $n$-th order polynomial, $P_n(t) = b_0 + b_1t + \cdots +b_nt^n$, we substitute in input output pairs, $(t_i, \hat{f}_i)$, giving
                    $$
                    \begin{align*}  
                    \hat{f}_1 &= b_0 + b_1(t_1) + \cdots +b_nt_1^n\\
                            &\cdots\\
                    \hat{f}_m &= b_0 + b_1(t_m) + \cdots +b_nt_m^n
                    \end{align*}
                    $$

                    Recognising that this a system of linear equations we can instead describe it with the notation
                    $$
                    \begin{align}
                    \hat{f} &= A b 
                    \end{align}
                    $$
                    where $A$ is a matrix containing the various powers of the input data (called the Vandermonde matrix), $b$ is a vector containing the to be determined polynomial coefficients, and $\hat{f}$ is a vector of our output data.

                    If $A$ is non-singular (i.e., invertible; this is guaranteed for a Vandermonde matrix with unique $t_i$) a solution to this system exists, namely $b = A^{-1}\hat{f}$.

                    There are various methods of finding the inverse of a matrix; in this instance we can use the singular value decomposition of $A$. For real-valued matrices the singular value decomposition is a factorisation of the form 
                    $$
                    \begin{align*}
                    A = U \Sigma V^T
                    \end{align*}
                    $$
                    with the properties that $U$ and $V^T$ are unitary (this means that the inverse of these matrices is their transposes), with dimensions $m\times m$ and $n \times n$, respectively. And $\Sigma$ is a $m\times n$ diagonal matrix, whose entries are descending singular values of $A$. 
                    
                    Substituting this into $(2)$ gives
                    $$
                    \begin{align}
                    \hat{f}(t) &= U \Sigma V^T b 
                    \end{align}
                    $$
                    
                    Since, inverting unitary and diagonal matrices is straightforward we now have an algorithm for solving our system of equations. First, left-multiplying $(3)$ by $U^T$ gives
                    $$
                    \begin{align*}
                    U^T\hat{f}(t) &= U^TU\Sigma V^T b \\
                    &= \Sigma V^T b
                    \end{align*}
                    $$
                    
                    Next, left-multiply by the inverse of $\Sigma$ which will just be itself with the diagonal entries reciprocated. 
                    $$
                    \begin{align*}
                    \Sigma^{-1} U^T \hat{f}(t) &= V^T b
                    \end{align*}
                    $$

                    Finally, left-multiply by $V$ to get the solution 
                    $$
                    \begin{align*}
                    V\Sigma^{-1} U^T \hat{f}(t) &= b
                    \end{align*}
                    $$

                    The theory can be put to practice with the following MATLAB code (it works in Octave too, though the axes' labels don't format nicely and for large enough $n$ Octave's svd function is not numerically stable):
                    ''')
        st.code('''
        clearvars

        % Set m and n
        m = 30-1; % 30 data points
        n = 15; % degree 15 polynomial

        % Compute t and f(t). From here on, single precision will be used
        t = single([0:m]/m);
        f = 2 + cos(8*t) + sin(16*t);
        %{
        To the true data add random numbers normally distributed with mean zero and variance of 0.05.
        For reproducibility also specify the seed and the generator used.
        https://au.mathworks.com/help/matlab/math/random-numbers-with-specific-mean-and-variance.html
        %}
        rng(42,'twister');
        f_hat = f + sqrt(0.05).*randn(1, m+1, 'single');
        f_hat_vec = f_hat'; % Transpose, so that it is a column vector

        % Create A, whose i-th column is t^i
        i = single([0:n]);
        A = (transpose(t)).^i;

        % Step 0. Compute reduced SVD using MATLAB's svd function
        [U, S, V] = svd(A, 'econ');

        % Step 1. Let c be the result
        c = (U')*f_hat_vec;

        % Step 2. Let d be the result
        Sd = diag(S);
        inv_Sd = 1.0./Sd;
        d = inv_Sd.*c;

        % Step 3. Finally find the coefficient vector b = Vd
        b = V*d;

        % Evaluate P_n(t) with this b
        Pt = A*b;

        % Plot of the data and the polynomial
        figure(1)
        plot(t, Pt, 'r--.')
        hold on
        plot(t, f, 'k--x')
        plot(t, f_hat, 'b--.')
        xlabel('$Inputs (t)$','Interpreter','latex')
        ylabel('Outputs','Interpreter','latex')
        legend('$P_{15}(t)$','$f(t)$','$\hat{f}(t)$','Interpreter','latex','Location','southeast','FontSize',14)
        title('When $n=15$','Interpreter','latex')
        ''', language="matlab")
        st.markdown(r'''
        When $n$ is set to $30$, the resulting polynomial overfits the perturbed data (see Figure 1 below).
        ''')   
        st.image(Image.open("media/plot30-1.jpg"), caption='Figure 1')
        st.markdown('''
        Or when run in Octave (with different random numbers) the resulting polynomial is incredibly poor (Octave's svd seems to be innacurate in producing the last singular values).
        ''')   
        st.image(Image.open("media/plot30-1-o.jpg"), caption='Figure 2')
        st.markdown(r'''
        Both these issues (overfitting and numerical instability) are overcome by finding a polynomial with lower degree. We can do this by either setting $n$ much smaller (since this specifies the polynomial degree) and re-running the script, or by setting small singular values to be zero and recomputing $Ab$. Before demonstrating this, a brief justification.
        
        Consider again the SVD of $A$, if we split $\Sigma$ into one matrix per singular value with all other entries being zero, i.e. the $i$-th such matrix can be described as $\Sigma_i = \text{diag}(0,\cdots, \sigma_i,\cdots, 0)$ then we can write 
        $$
        \begin{align*}
        A &= U(\Sigma_1 + \cdots + \Sigma_n)V^T 
        \end{align*}
        $$

        Focusing on the first two terms, notice that a matrix times a diagonal matrix with entries of all zero except for one will return the $i$-th column with entries multiplied by $\sigma_i$ with all other columns simply containing zeros. The non-zero column of each of the resulting matrices, when multiplied with $V^T$ multiplies with the $i$-th row like an outer product. Allowing us to write
        $$
        \begin{align*}
        A &= \sum_{i=1}^n \sigma_i u_i v_i^T
        \end{align*}
        $$
        
        Intuitively, for $\sigma_i\approx 0$ the corresponding matrix in the above expression is approximately entirely comprised of zeros, hence discarding small singular values will still give a good approximation of $A$.
        
        In MATLAB setting a lower $n$ gave
        ''')
        st.image(Image.open("media/plot8-1.jpg"), caption='Figure 1')
        st.markdown(r'''
        In Octave after inverting $\Sigma$, keeping only the first eleven singular values non-zero and continuing the script gives
        ''')
        st.image(Image.open("media/plot10-o.jpg"), caption='Figure 1')
        st.markdown(r'''
        To measure how good the fit is in this last example, the $2$-norm between the polynomial and the perturbed data is 1.08, between the polynomial and the 'true' data it is similar at 1.12, both are smaller than the amount of perturbation 1.29 (as measured by the 2-norm again).
        ''')

# Call and thereby display this page
if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
    captcha_control()
else:
    Comp_Math_page()
