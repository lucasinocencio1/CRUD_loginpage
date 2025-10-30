import streamlit as st
import os
from dotenv import load_dotenv
from src.widgets import __login__

# Load environment variables
load_dotenv()

# Get Courier auth token from environment
courier_token = os.getenv("COURIER_AUTH_TOKEN")
if not courier_token:
    st.error("COURIER_AUTH_TOKEN dont found in the .env file")
    st.stop()

__login__obj = __login__(auth_token = courier_token,
                    company_name = "Kraken_IA",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
username= __login__obj.get_username()

if LOGGED_IN == True:

   st.markdown("Your Streamlit Application Begins here!")
   st.markdown(st.session_state)
   st.write(username)
