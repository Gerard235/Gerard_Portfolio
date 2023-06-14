import streamlit as st
import sys
sys.path.append("./gerard_portfolio")
from captcha1 import captcha_control


captcha_control()


def Data_Projects_page():
    st.title("Gerard's web portfolio")
    st.text('Come back soon')

# Call and thereby display this page
if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
    captcha_control()
else:
    Data_Projects_page()
