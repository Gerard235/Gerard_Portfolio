import streamlit as st
import sys
sys.path.append("./gerard_portfolio")
from captcha1 import captcha_control

captcha_control()


def other_page():
    st.title("Gerard's web portfolio")
    st.text('placeholder equations')
    st.latex(r'''
    \frac{dS}{dt} = \mu N - \frac{\beta S I}{N} - \mu S - \kappa S \quad\quad\quad \frac{dE}{dt}=\frac{\beta S I }{N} - \sigma E - \mu E 
    ''')
    st.latex(r'''
    \frac{dI}{dt} = \sigma E - \mu I - \gamma I \quad\quad\quad \frac{dR}{dt}=\gamma I - \mu R
    \quad\quad\quad \frac{dV}{dt} = \kappa S - \mu V
    ''')


# Call and thereby display this page
if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
    captcha_control()
else:
    other_page()
