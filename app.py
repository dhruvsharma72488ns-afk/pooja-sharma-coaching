import streamlit as st
import json
import os
import random
import string
import datetime

st.set_page_config(page_title="Pooja Sharma Coaching Portal", page_icon="🎓", layout="wide")

USERS_FILE = "users.json"
STUDENTS_FILE = "students.json"

def load_data(filename):
    if not os.path.exists(filename):
        return [] if filename == STUDENTS_FILE else {}
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data
    except:
        return [] if filename == STUDENTS_FILE else {}

def save_data(filename, data):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")

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
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None
if "show_form" not in st.session_state:
    st.session_state.show_form = True

if "users_db" not in st.session_state:
    st.session_state.users_db = load_data(USERS_FILE)
if "students_db" not in st.session_state:
    loaded_students = load_data(STUDENTS_FILE)
    st.session_state.students_db = loaded_students if isinstance(loaded_students, list) else []

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
                    users[clean_reg_user] = {"password": reg_pass, "role": "Admin"}
                    save_data(USERS_FILE, users)
                    st.session_state.users_db = users
                    st.success("Account successfully ban gaya! Ab aap Login kar sakte hain.")
                    st.session_state.captcha_code = generate_captcha()
                    st.session_state.page_choice = "🔐 Login"
                    st.rerun()

else:
    # Header Control Bar
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown("### 👩‍🏫 WELCOME POOJA MAM")
    with top_col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.edit_index = None
            st.rerun()
            
    st.markdown("---")
    
    # Toggle button to show/hide form
    btn_text = "👁️ Hide Data Feed Form" if st.session_state.show_form else "📝 Show Data Feed Form"
    if st.button(btn_text):
        st.session_state.show_form = not st.session_state.show_form
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)

    # Main Grid Layout
    if st.session_state.show_form:
        form_col, data_col = st.columns([1.2, 2])
    else:
        data_col = st.container()

    # FORM SECTION
    if st.session_state.show_form:
        with form_col:
            st.markdown("#### 📝 Student Data Feed Form")
            
            edit_data = {}
            if st.session_state.edit_index is not None and st.session_state.edit_index < len(st.session_state.students_db):
                edit_data = st.session_state.students_db[st.session_state.edit_index]
                st.info(f"Editing: {edit_data.get('Student Name', '')}")

            with st.form("student_form", clear_on_submit=False):
                s_name = st.text_input("Student Name *", value=edit_data.get("Student Name", ""))
                
                class_options = [f"{i}th Class" if i > 3 else (f"{i}st Class" if i==1 else (f"{i}nd Class" if i==2 else f"{i}rd Class")) for i in range(1, 13)]
                default_class_idx = class_options.index(edit_data.get("Class")) if edit_data.get("Class") in class_options else 0
                s_class = st.selectbox("Class *", class_options, index=default_class_idx)
                
                s_school = st.text_input("School Name *", value=edit_data.get("School", ""))