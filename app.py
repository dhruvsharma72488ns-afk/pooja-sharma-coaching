import streamlit as st
import json
import os
import random
import string

st.set_page_config(page_title="Pooja Sharma Coaching Portal", page_icon="🎓", layout="wide")

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        st.error(f"Error saving user: {e}")

def generate_captcha():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

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
    st.session_state.captcha_code = generate_captcha()
if "recovered_password" not in st.session_state:
    st.session_state.recovered_password = None

if "users_db" not in st.session_state:
    st.session_state.users_db = load_users()
else:
    file_users = load_users()
    st.session_state.users_db.update(file_users)

users = st.session_state.users_db

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🎓 POOJA SHARMA COACHING CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Classes 1st to 12th | Excellence in Education</p>", unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.session_state.page_choice in ["🔐 Login", "📝 Create Account"]:
            st.session_state.page_choice = st.radio("Choose Action", ["🔐 Login", "📝 Create Account"], horizontal=True, label_visibility="collapsed", index=0 if st.session_state.page_choice=="🔐 Login" else 1)
            st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.page_choice == "🔐 Login":
            st.subheader("🔐 Login to Your Account")
            
            login_user = st.text_input("Username", key="l_user")
            login_pass = st.text_input("Password", type="password", key="l_pass")
            
            if st.button("Login Now", type="primary", use_container_width=True):
                clean_login_user = login_user.strip()
                matched_user = next((u for u in users if u.strip().lower() == clean_login_user.lower()), None)
                
                if matched_user and users[matched_user]["password"] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = matched_user
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Forgot Password?", use_container_width=True):
                st.session_state.page_choice = "🔑 Forgot Password Step 1"
                st.session_state.recovered_password = None
                st.rerun()

        elif st.session_state.page_choice == "🔑 Forgot Password Step 1":
            st.subheader("🔑 Enter Username to Recover Password")
            
            rec_user = st.text_input("Username", key="rec_user_input")
            
            if st.button("Find Password", type="primary", use_container_width=True):
                clean_rec_user = rec_user.strip()
                matched_user = next((u for u in users if u.strip().lower() == clean_rec_user.lower()), None)
                
                if matched_user:
                    st.session_state.recovered_password = users[matched_user]['password']
                    st.session_state.page_choice = "🔑 Forgot Password Step 2"
                    st.rerun()
                else:
                    st.error("Yeh username system mein nahi mila! Kripya sahi username dalein.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Back to Login", use_container_width=True):
                st.session_state.page_choice = "🔐 Login"
                st.rerun()

        elif st.session_state.page_choice == "🔑 Forgot Password Step 2":
            st.subheader("🔒 Your Recovered Password")
            
            st.success(f"Your Password = **{st.session_state.recovered_password}**")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔙 Back to Login", type="primary", use_container_width=True):
                st.session_state.recovered_password = None
                st.session_state.page_choice = "🔐 Login"
                st.rerun()

        else:
            st.subheader("📝 Create a New Account")
            
            reg_user = st.text_input("Choose Username", key="r_user")
            reg_pass = st.text_input("Choose Password", type="password", key="r_pass")
            reg_repass = st.text_input("Re-enter Password", type="password", key="r_repass")
            
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"<div style='background-color: #262730; padding: 10px; border-radius: 8px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 4px; color: #00ffcc;'>{st.session_state.captcha_code}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄"):
                    st.session_state.captcha_code = generate_captcha()
                    st.rerun()
            
            user_captcha = st.text_input("Enter Code Shown Above", key="r_captcha")
            
            if st.button("Register Account", type="primary", use_container_width=True):
                clean_reg_user = reg_user.strip()
                if not clean_reg_user or not reg_pass or not reg_repass or not user_captcha:
                    st.warning("Sabhi fields bharna zaroori hai!")
                elif reg_pass != reg_repass:
                    st.error("Passwords match nahi kar rahe hain!")
                    st.session_state.captcha_code = generate_captcha()
                    st.rerun()
                elif user_captcha != st.session_state.captcha_code:
                    st.error("Galat Code! Kripya sahi code enter karein.")
                    st.session_state.captcha_code = generate_captcha()
                    st.rerun()
                elif any(u.strip().lower() == clean_reg_user.lower() for u in users):
                    st.error("Yeh Username pehle se maujood hai! Dusra chunein.")
                    st.session_state.captcha_code = generate_captcha()
                    st.rerun()
                else:
                    users[clean_reg_user] = {"password": reg_pass, "role": "Student"}
                    save_users(users)
                    st.session_state.users_db = users
                    st.success("Account successfully ban gaya! Ab aap Login kar sakte hain.")
                    st.session_state.captcha_code = generate_captcha()
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