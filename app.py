import streamlit as st
import json
import os

st.set_page_config(page_title="Pooja Sharma Coaching", page_icon="🎓", layout="wide")

USERS_FILE = "users.json"

# Helper functions to handle JSON
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

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Main App Logic
st.title("🎓 POOJA SHARMA COACHING CENTER")
st.markdown("---")

users = load_users()

if not st.session_state.logged_in:
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🔑 Recover Password"])

    with tab1:
        st.subheader("Login to Your Account")
        login_user = st.text_input("Username", key="l_user")
        login_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login", type="primary"):
            if login_user in users and users[login_user]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    with tab2:
        st.subheader("Create a New Account")
        reg_user = st.text_input("Choose Username", key="r_user")
        reg_pass = st.text_input("Choose Password", type="password", key="r_pass")
        reg_role = st.selectbox("Role", ["Student", "Teacher", "Admin"])
        if st.button("Register"):
            if not reg_user or not reg_pass:
                st.warning("Please fill all fields")
            elif reg_user in users:
                st.error("Username already exists!")
            else:
                users[reg_user] = {"password": reg_pass, "role": reg_role}
                save_users(users)
                st.success("Account registered successfully! Please login.")

    with tab3:
        st.subheader("Recover Password")
        rec_user = st.text_input("Enter Username", key="rec_user")
        if st.button("Get Password"):
            if rec_user in users:
                st.info(f"Your password is: **{users[rec_user]['password']}**")
            else:
                st.error("Username not found!")

else:
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    st.sidebar.markdown(f"**Role:** {users.get(st.session_state.username, {}).get('role', 'User')}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.subheader("📌 Student Management Dashboard")
    st.write("Welcome to the Pooja Sharma Coaching App.")
    
    # Simple JSON data display
    st.json(users)