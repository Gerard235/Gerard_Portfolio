import streamlit as st
from captcha.image import ImageCaptcha
import random, string

# Credit for this code goes to alessandro_ciciarell
# https://discuss.streamlit.io/t/streamlit-captcha-integration/38318

# define the function for the captcha control
def captcha_control():
    
    length_captcha = 4
    width = 200
    height = 150
    
    # control if the captcha is correct
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        st.title("Completely Automated Public Turing test to tell Computers and Humans Apart")
        
        # define the session state for control if the captcha is correct
        st.session_state['controllo'] = False
        col1, col2 = st.columns(2)
        
        # define the session state for the captcha text because it doesn't change during refreshes 
        if 'Captcha' not in st.session_state:
                st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))
        print("the captcha is: ", st.session_state['Captcha'])
        
        # setup the captcha widget
        image = ImageCaptcha(width=width, height=height)
        data = image.generate(st.session_state['Captcha'])
        col1.image(data)
        capta2_text = col2.text_area('Enter captcha text', height=30)
        
        
        if st.button("Verify the code"):
            print(capta2_text, st.session_state['Captcha'])
            capta2_text = capta2_text.replace(" ", "")
            # if the captcha is correct, the controllo session state is set to True
            if st.session_state['Captcha'].lower() == capta2_text.lower().strip():
                del st.session_state['Captcha']
                col1.empty()
                col2.empty()
                st.session_state['controllo'] = True
                st.experimental_rerun() 
            else:
                # if the captcha is wrong, the controllo session state is set to False and the captcha is regenerated
                st.error("🚨 The captcha code is incorrect, please try again.")
                del st.session_state['Captcha']
                del st.session_state['controllo']
                st.experimental_rerun()
        else:
            # wait for the button click
            st.stop()
