import streamlit as st
from captcha.image import ImageCaptcha
import random, string
import plotly.express as px
import plotly.io as pio
import numpy as np
from captcha1 import captcha_control


st.set_page_config(layout="wide", initial_sidebar_state="auto")


# call the function for the captcha control
captcha_control()

# ... 
def main_page():
    st.title("Gerard's web portfolio")
    st.markdown('I like data analysis/science, computational mathematics, and a bunch of other stuff. This page has a brief exhibit for each of these areas. You can navigate to pages with more examples using the sidebar.')

    quote = r"'The rise of powerful AI will either be the best or the worst thing ever to happen to humanity. We do not yet know which.' Stephen Hawking"
    st.markdown("'*... the Japanese, they’re doing some wonderful work with artificial intelligence, now, you combine that with some animatronics from the imagineers over at Disney, next thing you know, we’re playing Halo with a multi-lingual Abraham Lincoln.*' Sheldon Cooper, season 2 episode 4 of The Big Bang Theory.")
    st.divider()

    st.subheader('Data analysis/science')
    st.markdown('After my favourite budgeting app ceased operating, I built my own solution. This project uses the [Basiq API](https://www.basiq.io/) to retrieve data, Python and R scripts to process and generate insights from that data, and [Streamlit](https://streamlit.io/) for the web app.')
    st.markdown('Below are two example charts based on test user data from Basiq.')
    l, r = st.columns(2)
    with l:
        fig0 = pio.read_json("media/fig0_json")
        st.plotly_chart(fig0)
    with r:
        fig = pio.read_json("media/fig_json")
        st.plotly_chart(fig)
    st.divider()

    

    st.subheader('Computational mathematics')
    st.markdown("Is the study of the techniques and algorithms needed to solve mathematical problems with computers, especially those problems that can only be solved with the processing power of computers. Ensuring that calculations are completed accurately and quickly is crucial. However, these two qualities need to be balanced, as the following simple example illustrates.") 
    st.markdown("To quickly evaluate polynomials, NumPy's [polyval](https://numpy.org/doc/stable/reference/generated/numpy.polyval.html) and other implementations use Horner's scheme. This code plots $q(x) = (x - 2)^9$ using Horner's method, as well as direct approaches on the expanded and factorised forms of this polynomial.")
    col1, col2 = st.columns(2)
    with col1:
        code = ''' 
        # Qx is Horner's method, Q1x is direct computation of the expanded polynomial, and qx is direct computation of the factored polynomial
        import numpy as np
        import plotly.express as px
        
        n = 1000
        x = np.linspace(1.92, 2.08, n)
        Q = [1, -18, 144, -672, 2016, -4032, 5376, -4608, 2304, -512]
        Qx = np.polyval(Q, x) # Polyval uses Horner's method
        Q1x = x**9 - 18*x**8 + 144*x**7 - 672*x**6 + 2016*x**5 - 4032*x**4 + 5376*x**3 - 4608*x**2 + 2304*x - 512
        qx = np.power(x - 2, 9)

        plot1 = px.line() 
        plot1.add_scatter(x=x, y=Q1x, mode='lines', name='Q1(x)', line=dict(color='yellow'))
        plot1.add_scatter(x=x, y=Qx, mode='lines', name='Q(x)', line=dict(color='red'))  
        plot1.add_scatter(x=x, y=qx, mode='lines', name='q(x)', line=dict(color='blue'))
        st.plotly_chart(plot1)
        '''
        st.code(code, language='python')
        st.markdown("To learn more about why this occurs see introductions to computational mathematics/scientific computing/numerical methods. Unaddressed errors like this can lead to real world [disasters](http://ta.twi.tudelft.nl/users/vuik/wi211/disasters.html).")

        

    with col2:
        n = st.slider("As you increase the number of inputs (i.e., computations performed), observe that the accuracy decreases.", min_value=100, max_value=5000, value=1000, step=50)
        x = np.linspace(1.92, 2.08, n)
        Q = [1, -18, 144, -672, 2016, -4032, 5376, -4608, 2304, -512]
        Qx = np.polyval(Q, x)
        Q1x = x**9 - 18*x**8 + 144*x**7 - 672*x**6 + 2016*x**5 - 4032*x**4 + 5376*x**3 - 4608*x**2 + 2304*x - 512
        qx = np.power(x - 2, 9)
        

        plot1 = px.line() 
        plot1.add_scatter(x=x, y=Q1x, mode='lines', name='Q1(x)', line=dict(color='yellow'))
        plot1.add_scatter(x=x, y=Qx, mode='lines', name='Q(x)', line=dict(color='red'))  
        plot1.add_scatter(x=x, y=qx, mode='lines', name='q(x)', line=dict(color='blue'))
        st.plotly_chart(plot1)

    st.markdown("###### Moral of the story: do not blindly trust a computer's outputs; a lesson which will be ever more pertinent with the advent of AI.")
    st.divider()

    st.subheader('Other')
    st.markdown("I enjoy kayaking.")
    video_file = open('media/kayaking.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)




    st.divider()
    if st.button("Go back to the CAPTCHA page"):
        del st.session_state['controllo']
        st.experimental_rerun()


# Call and thereby display the main page
if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
    captcha_control()
else:
    main_page()
