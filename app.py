import streamlit as st
import json
import os
import datetime

st.set_page_config(page_title="Pooja Sharma Coaching Portal", page_icon="🎓", layout="wide")

USERS_FILE = "users.json"
STUDENTS_FILE = "students.json"

def load_users():
    default_users = {"pooja": {"password": "12345", "role": "Admin"}, "dhruv": {"password": "1234", "role": "Admin"}}
    if not os.path.exists(USERS_FILE):
        return default_users
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return default_users
            if "pooja" not in data:
                data["pooja"] = {"password": "12345", "role": "Admin"}
            return data
    except:
        return default_users

def save_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        pass

def load_students():
    if not os.path.exists(STUDENTS_FILE):
        return []
    try:
        with open(STUDENTS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_students(students):
    try:
        with open(STUDENTS_FILE, "w") as f:
            json.dump(students, f, indent=4)
    except Exception as e:
        pass

# Custom Education Theme CSS
st.markdown("""
<style>
    .stAppHeader {
        display: none;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    .stExpander {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
    }
    div[data-testid="stForm"] {
        background-color: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(129, 140, 248, 0.2);
        border-radius: 10px;
        padding: 15px;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page_choice" not in st.session_state:
    st.session_state.page_choice = "🔐 Login"
if "recovered_password" not in st.session_state:
    st.session_state.recovered_password = None
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

if "users_db" not in st.session_state:
    st.session_state.users_db = load_users()

users = st.session_state.users_db
students_db = load_students()

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🎓 POOJA SHARMA COACHING CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Classes 1st to 12th | Excellence in Education</p>", unsafe_allow_html=True)
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
                clean_login_user = login_user.strip().lower()
                matched_user = next((u for u in users if u.strip().lower() == clean_login_user), None)
                
                if matched_user and str(users[matched_user]["password"]) == str(login_pass):
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
                clean_rec_user = rec_user.strip().lower()
                matched_user = next((u for u in users if u.strip().lower() == clean_rec_user), None)
                
                if matched_user:
                    st.session_state.recovered_password = users[matched_user]['password']