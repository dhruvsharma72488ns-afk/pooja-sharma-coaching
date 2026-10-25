import streamlit as st
import json
import os

st.set_page_config(page_title="Pooja Sharma Coaching", page_icon="🎓", layout="wide")

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

# Custom Styling to match your original HTML design
st.markdown("""
<style>
    .main {
        background-color: #f4f6f9;
    }
    .stAppHeader {
        display: none;
    }
    .card-box {
        background-color: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        max-width: 500px;
        margin: auto;
    }
    .title-header {
        color: #2c3e50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=unsafe_allow_html:=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

users = load_users()

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🎓 POOJA SHARMA COACHING CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Classes 1st to 12th | Excellence in Education</p>", unsafe_allow_html=True)
st.markdown("---")

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🔑 Recover Password"])

        with tab1:
            st.subheader("Login")
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

        with tab2:
            st.subheader("Create Account")
            reg_user = st.text_input("Choose Username", key="r_user")
            reg_pass = st.text_input("Choose Password", type="password", key="r_pass")
            reg_role = st.selectbox("Role", ["Student", "Teacher", "Admin"])
            if st.button("Register Account", use_container_width=True):
                if not reg_user or not reg_pass:
                    st.warning("Fields cannot be empty")
                elif reg_user in users:
                    st.error("Username already taken!")
                else:
                    users[reg_user] = {"password": reg_pass, "role": reg_role}
                    save_users(users)
                    st.success("Registration Complete! Please Login.")

        with tab3:
            st.subheader("Find Password")
            rec_user = st.text_input("Enter your Username", key="rec_user")
            if st.button("Recover", use_container_width=True):
                if rec_user in users:
                    st.info(f"Password for {rec_user}: **{users[rec_user]['password']}**")
                else:
                    st.error("User not found!")

else:
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.write(f"**Role:** {users.get(st.session_state.username, {}).get('role', 'Student')}")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.subheader(" Welcome to Student Portal")
    st.success(f"Hello {st.session_state.username}, welcome back to Pooja Sharma Coaching Center portal.")
    
    st.markdown("### 📊 Registered System Users")
    st.dataframe(users, use_container_width=True)