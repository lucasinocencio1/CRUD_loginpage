import re
import json
from trycourier import Courier
import secrets
from argon2 import PasswordHasher
import requests


ph = PasswordHasher() 

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

def check_usr_pass(email: str, password: str) -> bool:
    try:
        response = requests.post(f"{API_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            st.session_state["username"] = data.get("username", "")
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    try:
        response = requests.get(f"{API_URL}/users/email/{email_sign_up}")
        if response.status_code == 200:
            return False  # Email already exists
        return True
    except:
        return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    non_empty_check = non_empty_str_check(username_sign_up)
    if non_empty_check == False:
        return None
    
    try:
        response = requests.get(f"{API_URL}/users")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                if user.get('username') == username_sign_up:
                    return False
    except:
        pass
    
    return True


def register_new_usr(name: str, email: str, username: str, password: str, department: str):
    try:
        response = requests.post(f"{API_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password,
            "department": department
        })
        if response.status_code == 200:
            st.success("Registro exitoso!")
        else:
            st.error(response.json().get("detail", "Error al registrar usuario."))
    except Exception as e:
        st.error(f"Error de conexión: {e}")


def check_username_exists(user_name: str) -> bool:
    """
    Checks if the username exists in the database.
    """
    try:
        response = requests.get(f"{API_URL}/users")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                if user.get('username') == user_name:
                    return True
    except:
        pass
    return False
        

def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the database.
    """
    try:
        response = requests.get(f"{API_URL}/users/email/{email_forgot_passwd}")
        if response.status_code == 200:
            user = response.json()
            return True, user.get('username', '')
    except:
        pass
    return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(auth_token: str, username_forgot_passwd: str, email_forgot_passwd: str, company_name: str, random_password: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(auth_token = auth_token)

    resp = client.send_message(
    message={
        "to": {
        "email": email_forgot_passwd
        },
        "content": {
        "title": company_name + ": Login Password!",
        "body": "Hi! " + username_forgot_passwd + "," + "\n" + "\n" + "Your temporary login password is: " + random_password  + "\n" + "\n" + "{{info}}"
        },
        "data":{
        "info": "Please reset your password at the earliest for security reasons."
        }
    }
    )


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    try:
        response = requests.put(f"{API_URL}/users/email/{email_}", json={
            "password": random_password
        })
        if response.status_code == 200:
            st.success("Password changed successfully")
        else:
            st.error("Failed to change password")
    except Exception as e:
        st.error(f"Error changing password: {e}")
    

def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the email when 
    resetting the password.
    """
    try:
        response = requests.post(f"{API_URL}/auth/login", json={
            "email": email_reset_passwd,
            "password": current_passwd
        })
        if response.status_code == 200:
            return True
    except:
        pass
    return False
