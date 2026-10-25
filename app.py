import streamlit as st
import json
import os
import random

st.set_page_config(page_title="Pooja Sharma Coaching Portal", page_icon="🎓", layout="wide")

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Hide Streamlit header
st.markdown("""
<style>
    .stAppHeader {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page_choice" not in st.session_state:
    st.session_state.page_choice = "🔐 Login"
if "captcha_code" not in st.session_state:
    st.session_state.captcha_code = str(random.randint(1000, 9999))

users = load_users()

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🎓 POOJA SHARMA COACHING CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Classes 1st to 12th | Excellence in Education</p>", unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.session_state.page_choice = st.radio("Choose Action", ["🔐 Login", "📝 Create Account"], horizontal=True, label_visibility="collapsed", index=0 if st.session_state.page_choice=="🔐 Login" else 1)
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.page_choice == "🔐 Login":
            st.subheader("🔐 Login to Your Account")
            
            login_user = st.text_input("Username", key="l_user")
            login_pass = st.text_input("Password", type="password", key="l_pass")
            
            if st.button("Login Now", type="primary", use_container_width=True):
                if login_user in users and users[login_user]["password"] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Forgot Password?", use_container_width=True):
                if login_user in users:
                    st.info(f"Aapka password hai: **{users[login_user]['password']}**")
                else:
                    st.warning("Pehle upar Username dalein, phir Forgot Password dabayein.")

        else:
            st.subheader("📝 Create a New Account")
            
            reg_user = st.text_input("Choose Username", key="r_user")
            reg_pass = st.text_input("Choose Password", type="password", key="r_pass")
            reg_repass = st.text_input("Re-enter Password", type="password", key="r_repass")
            
            # Captcha Section
            st.markdown(f"### 🔏 Captcha Code: `{st.session_state.captcha_code}`")
            user_captcha = st.text_input("Enter Captcha Code Above", key="r_captcha")
            
            if st.button("Register Account", type="primary", use_container_width=True):
                if not reg_user or not reg_pass or not reg_repass or not user_captcha:
                    st.warning("Sabhi fields bharna zaroori hai!")
                elif reg_pass != reg_repass:
                    st.error("Passwords match nahi kar rahe hain!")
                elif user_captcha != st.session_state.captcha_code:
                    st.error("Galat Captcha! Kripya sahi captcha dalein.")
                    st.session_state.captcha_code = str(random.randint(1000, 9999))
                elif reg_user in users:
                    st.error("Yeh Username pehle se maujood hai! Dusra chunein.")
                    st.session_state.captcha_code = str(random.randint(1000, 9999))
                else:
                    users[reg_user] = {"password": reg_pass, "role": "Student"}
                    save_users(users)
                    st.success("Account successfully ban gaya! Ab aap Login kar sakte hain.")
                    # Reset captcha and switch back to login page automatically
                    st.session_state.captcha_code = str(random.randint(1000, 9999))
                    st.session_state.page_choice = "🔐 Login"
                    st.rerun()

else:
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.write(f"**Role:** {users.get(st.session_state.username, {}).get('role', 'Student')}")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.subheader("Welcome to Student Portal")
    st.success(f"Hello {st.session_state.username}, aapka swagat hai!")
    
    st.markdown("### 📊 Registered System Users")
    st.dataframe(users, use_container_width=True)