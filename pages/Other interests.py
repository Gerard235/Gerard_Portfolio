import streamlit as st
import sys
sys.path.append("./gerard_portfolio")

st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Other interests")

def other_page():
    st.title("Gerard's web portfolio")

    with st.expander("The Fibonacci sequence, linear algebra, and Project Euler"):
        st.markdown(r'''
                    It is possible to write a $2$x$2$ matrix $A$ that models a Fibonacci sequence as a discrete dynamical system. After fixing initial values $a_0$ and $a_1$, the subsequent terms of a Fibonacci sequence are defined as follows
                    $$
                    \begin{align}  
                    a_{i+1}=a_{i-1}+a_i    
                    \end{align}
                    $$
                    The form of the linear system we wish to set-up is given by
                    $$
                    \begin{align}
                    \begin{bmatrix}
                    a_{i+1} \\
                    a_i
                    \end{bmatrix}
                    =
                    A\begin{bmatrix}
                    a_i\\
                    a_{i-1}
                    \end{bmatrix}
                    \end{align}
                    $$
                    From $(2)$ it follows that the above system is equivalent to
                    $$
                    \begin{align*}
                    a_{i+1}&=a_i+a_{i-1} \\
                    a_i&=a_i+0\cdot a_{i-1} 
                    \end{align*}
                    $$
                    Which can be written as
                    $$
                    \begin{align*}
                    \begin{bmatrix}
                    a_{i+1} \\
                    a_i
                    \end{bmatrix}
                    =\begin{bmatrix}
                    1 & 1 \\
                    1 & 0
                    \end{bmatrix}
                    \begin{bmatrix}
                    a_i\\
                    a_{i-1}
                    \end{bmatrix}
                    \end{align*}
                    $$
                    Hence, A is the matrix
                    $$
                    \begin{align*}
                    A=\begin{bmatrix}
                    1 & 1 \\
                    1 & 0
                    \end{bmatrix}
                    \end{align*}
                    $$
                    In order to simplify our linear system, it is useful to find the Eigenvalues and Eigenvectors of $A$, and then diagonalise this matrix. To find the Eigenvalues we find the characteristic equation by finding solutions to $\det(A-\lambda I)=0$.
                    $$
                    \begin{align*}
                    \begin{vmatrix}
                    1- \lambda & 1 \\
                    1 & - \lambda
                    \end{vmatrix}
                    &=0 \\
                    (1-\lambda)\cdot -\lambda -1&=0 \\
                    \lambda^2-\lambda-1&=0
                    \end{align*}
                    $$
                    Note: the discriminant in this case is positive, $(-1)^2-4(1)(-1)=5$; so there will be two real valued roots (that is, two real valued Eigenvalues). By the quadratic equation these are
                    $$
                    \begin{align*}
                    \lambda &=\frac{1\pm\sqrt{(-1)^2-4(1)(-1)}}{2(1)} \\
                    &=\frac{1\pm\sqrt{5}}{2} \\
                    \lambda_1=\frac{1+\sqrt{5}}{2} \qquad&\qquad\qquad
                    \lambda_2=\frac{1-\sqrt{5}}{2}\end{align*}
                    $$
                    Using these Eigenvalues we can determine the associated Eigenvectors.
                    $$
                    \begin{align*}
                    E_{\lambda1}&=\nul
                    \begin{bmatrix}
                    1 - \frac{1+\sqrt{5}}{2} & 1 \\
                    1 & -\frac{1+\sqrt{5}}{2}
                    \end{bmatrix}\\
                    &=\nul
                    \begin{bmatrix}
                    \frac{1-\sqrt{5}}{2} & 1 \\
                    1 & -\frac{1+\sqrt{5}}{2}
                    \end{bmatrix} \\
                    &=\nul
                    \begin{bmatrix}
                    \frac{1-\sqrt{5}}{2} & 1 \\
                    \frac{1-\sqrt{5}}{2} & 1
                    \end{bmatrix} &\left(R2 \cdot \frac{1-\sqrt{5}}{2}\right) \\
                    &=\nul
                    \begin{bmatrix}
                    \frac{1-\sqrt{5}}{2} & 1 \\
                    0 & 0
                    \end{bmatrix} \\
                    &=\nul
                    \begin{bmatrix}
                    1 & -\frac{1+\sqrt{5}}{2} \\
                    0 & 0
                    \end{bmatrix} &\left(R1\cdot-\frac{1+\sqrt{5}}{2}\right) \\
                    &=\span\begin{pmatrix}
                    \frac{1+\sqrt{5}}{2}\\
                    1
                    \end{pmatrix}
                    \end{align*}
                    $$
                    This process is repeated for $E_{\lambda2}$ giving
                    $$
                    \begin{align*}
                    E_{\lambda2}&=\nul\begin{bmatrix}
                    1-\frac{1-\sqrt{5}}{2} & 1 \\
                    1 & -\frac{1-\sqrt{5}}{2}
                    \end{bmatrix}\\
                    &=\span\begin{pmatrix}
                    \frac{1-\sqrt{5}}{2} \\
                    1
                    \end{pmatrix}
                    \end{align*}
                    $$
                    The diagonalisation of $A$ is given by $A=PDP^{-1}$. Where the columns of $P$ are the Eigenvectors determined above, $P^{-1}$ is simply the inverse of $P$, and $D$ is a diagonal matrix whose entries are the Eigenvalues above. The inverse of $P$ can be determined easily and is
                    $$
                    \begin{align*}
                    P^{-1}&=\frac{1}{\sqrt{5}}\begin{bmatrix}
                    1 & \frac{\sqrt{5}-1}{2}\\
                    -1 & \frac{1+\sqrt{5}}{2}
                    \end{bmatrix}\\
                    &=\begin{bmatrix}
                    \frac{\sqrt{5}}{5} & \frac{-\sqrt{5}+5}{10} \\
                    \frac{-\sqrt{5}}{5} & \frac{\sqrt{5}+5}{10}
                    \end{bmatrix} \tag*{Note: denominators have been rationalised}
                    \end{align*}
                    $$
                    Hence
                    $$
                    \begin{align*}
                    A&=\begin{bmatrix}
                    \frac{1+\sqrt{5}}{2} & \frac{-\sqrt{5}+1}{2}\\
                    1 & 1
                    \end{bmatrix}
                    \begin{bmatrix}
                    \frac{1+\sqrt{5}}{2} & 0 \\
                    0 & \frac{1-\sqrt{5}}{2}
                    \end{bmatrix}
                    \begin{bmatrix}
                    \frac{\sqrt{5}}{5} & \frac{-\sqrt{5}+5}{10} \\
                    \frac{-\sqrt{5}}{5} & \frac{\sqrt{5}+5}{10}
                    \end{bmatrix}
                    \end{align*} \\
                    $$
                    Now, recall that we are modelling a Fibonacci sequence as a discrete dynamical system of the form 
                    $$
                    \begin{align*}
                    \mathbf{x_{m+1}}&=A\mathbf{{x_m}}
                    \end{align*}
                    $$
                    Therefore finding the next term in the sequence is equivalent to
                    $$
                    \begin{align*}
                    \mathbf{x_{m+2}}&=A\mathbf{x_{m+1}} \\
                    &=AA\mathbf{x_m} \\
                    &=A^2\mathbf{x_m}
                    \end{align*}
                    $$
                    It is apparent that this process can be generalised to 
                    $$
                    \begin{align*}
                    \mathbf{x_{m+n}}=A^n\mathbf{x_m}
                    \end{align*}
                    $$
                    Setting \(m = 0\) gives
                    $$
                    \begin{align*}
                    \mathbf{x_{n}}=A^n\mathbf{x_0}
                    \end{align*}
                    $$
                    for $n = 1, 2, 3,...$. 

                    Furthermore, we can simplify this using the diagonalisation of $A$ from above, in which case we get
                    $$
                    \begin{align*}
                    A^n&=\left(PDP^{-1}\right)^n \\
                    &=PDP^{-1}\cdot PDP^{-1}\cdot PDP^{-1}\dots \\
                    &=PD^nP^{-1}
                    \end{align*}
                    $$
                    Finally, this allows us to write a formula for the $n$-th pair of terms (setting the first two terms to be 0 and 1)
                    $$
                    \begin{align*}
                    \mathbf{x_{n}}&=PD^nP^{-1}\begin{bmatrix}
                    1\\
                    0
                    \end{bmatrix}\\
                    &=\begin{bmatrix}
                    \frac{1+\sqrt{5}}{2} & \frac{-\sqrt{5}+1}{2}\\
                    1 & 1
                    \end{bmatrix}
                    \begin{bmatrix}
                    \frac{1+\sqrt{5}}{2} & 0 \\
                    0 & \frac{1-\sqrt{5}}{2}
                    \end{bmatrix}^n
                    \begin{bmatrix}
                    \frac{\sqrt{5}}{5} & \frac{-\sqrt{5}+5}{10} \\
                    \frac{-\sqrt{5}}{5} & \frac{\sqrt{5}+5}{10}
                    \end{bmatrix}
                    \begin{bmatrix}
                    1\\
                    0
                    \end{bmatrix}\\
                    &=\begin{bmatrix}
                    \frac{1+\sqrt{5}}{2} & \frac{-\sqrt{5}+1}{2}\\
                    1 & 1
                    \end{bmatrix}
                    \begin{bmatrix}
                    \left(\frac{1+\sqrt{5}}{2}\right)^n & 0 \\
                    0 & \left(\frac{1-\sqrt{5}}{2}\right)^n
                    \end{bmatrix}
                    \begin{bmatrix}
                    \frac{\sqrt{5}}{5} & \frac{-\sqrt{5}+5}{10} \\
                    \frac{-\sqrt{5}}{5} & \frac{\sqrt{5}+5}{10}
                    \end{bmatrix}
                    \begin{bmatrix}
                    1\\
                    0
                    \end{bmatrix}
                    \end{align*}
                    $$
                    ''')
        st.markdown(r'''
                    Though not a recommended approach to this problem, for a bit of fun, this formula can be used to solve Project Euler's problem number 2 (summing even Fibonacci terms less than 4 million). The following MATLAB code is a simple example:
                    ''')
        st.code('''
        % Find the sum of the even-valued Fibonacci terms less than four million.

        ind = 2:35;
        fibs = zeros(1, 35);
        fib = 1;

        for i = ind
            fib = (5^(0.5)/5)*( ((1+5^(0.5))/2)^i - ((1-5^(0.5))/2)^i );
            if fib < 4000000
                fibs(1, i-1) = fib;
            end
        end

        fibs = round(fibs, 0)
        remainder = rem(fibs,2);
        fibs(remainder==1) = []
        answer = sum(fibs)
        ''', language="matlab")

    with st.expander("Creating a simple executable file to change a desktop's background"):
        st.markdown(r'''
                    For fun, I shared some executable files with my friends which change a desktop's background to an image I'd selected. 
                    
                    First, the image needs to be converted to byte data. Then a simple python script uses this to change the background. Finally, make the python script into an executable file.

                    This code completes the first task.
                    ''')
        st.code(r'''
                import base64

                def pic2str(fileName, varName, outFileName):
                    # This function takes an image, converts that to byte data, and saves the result in a .py file with a variable name of your choice
                    # Credit for the original code goes to Clay at https://clay-atlas.com/us/blog/2020/11/04/python-en-package-pyinstaller-picture/
                    pic = open(fileName, 'rb')
                    content = '{} = {}\n'.format(varName, base64.b64encode(pic.read()))
                    pic.close()

                    with open(outFileName, 'a') as f:
                        f.write(content)
                        
                if __name__ == '__main__':
                pic2str('picture_filename.jpg', 'image_var_name', 'pic_as_str.py')
                ''', language="python")
        st.markdown(r'''
                    Having created 'pic_as_str.py', create a new Python script "change_wallpaper.py" with the code below.
                    ''')
        st.code(r'''
                import ctypes
                import os
                import base64
                from io import BytesIO
                from PIL import Image

                SPI_SETDESKWALLPAPER = 20

                # Import the image that had been saved as a string, save that as a jpg and then set it as the wallpaper
                from pic_as_str import image_var_name

                byte_data = base64.b64decode(image_var_name)
                image_data = BytesIO(byte_data)
                im = Image.open(image_data)
                image = im.save("saved.jpg")

                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath("saved.jpg"), 3)
                ''', language="python")
        st.markdown(r'''
                    On your local machine you can run the above script to test that it works. To turn this into an executable file, first open a command prompt and install PyInstaller with 
                    ''')
        st.code(r'''
                pip install pyinstaller
                ''', language="cmd")
        st.markdown(r'''
                    Then in the same directory as "change_wallpaper.py", run the command
                    ''')
        st.code(r'''
                pyinstaller --onefile change_wallpaper.py
                ''', language="cmd")
        st.markdown(r'''
                    Once complete there will be a new folder 'dist', with 'change_wallpaper.exe'. 
                    
                    Now you need to figure out how to get your friends to run this file on their PC.
                    ''')        

other_page()
