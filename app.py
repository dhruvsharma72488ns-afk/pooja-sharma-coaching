import streamlit as st

st.set_page_config(
    page_title="Pooja Sharma Coaching Center", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Permanent Credentials jo kabhi delete nahi honge
USERS = st.secrets.get("users", {"pooja": "12345"})

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("POOJA SHARMA COACHING CENTER")
st.markdown("Classes 1st to 12th | Excellence in Education")

# Jab user Login na ho
if not st.session_state.logged_in:
    st.subheader("🔑 Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login Now"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = "Pooja Mam" if username == "pooja" else username
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# Jab Login ho jaye (Main Student Details & Record Dashboard)
else:
    st.sidebar.success(f"Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.subheader(f"📊 Student Details & Records Portal - Welcome {st.session_state.username}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", "120")
    col2.metric("Active Classes", "1st to 12th")
    col3.metric("Pending Fees Status", "Clear")

    st.markdown("---")
    st.markdown("### 📋 Student Management Table")
    
    student_data = [
        {"Roll No": 101, "Student Name": "Aarav Kumar", "Class": "10th", "Subject": "Maths & Science", "Fee Status": "Paid"},
        {"Roll No": 102, "Student Name": "Ananya Sharma", "Class": "12th", "Subject": "Physics & Chemistry", "Fee Status": "Pending"},
        {"Roll No": 103, "Student Name": "Rohan Verma", "Class": "8th", "Subject": "All Subjects", "Fee Status": "Paid"},
    ]
    st.table(student_data)