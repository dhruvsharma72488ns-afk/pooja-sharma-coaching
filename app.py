import streamlit as st
import json
import os

st.set_page_config(page_title="Pooja Sharma Coaching - Login", page_icon="🎓", layout="wide")

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Hide Streamlit default header
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

users = load_users()

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🎓 POOJA SHARMA COACHING CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Classes 1st to 12th | Excellence in Education</p>", unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
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
        
        # Forgot Password text option
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Forgot Password?", use_container_width=True):
            if login_user in users:
                st.info(f"Aapka password hai: **{users[login_user]['password']}**")
            else:
                st.warning("Pehle upar sahi Username dalein, phir Forgot Password dabayein.")

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