import streamlit as st
import random

st.set_page_config(
    page_title="Pooja Sharma Coaching Center", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for users and login
if "users" not in st.session_state:
    # Default permanent user
    st.session_state.users = {"pooja": "12345"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Login"

# Captcha numbers generate karne ke liye
if "num1" not in st.session_state or "num2" not in st.session_state:
    st.session_state.num1 = random.randint(1, 9)
    st.session_state.num2 = random.randint(1, 9)

st.title("POOJA SHARMA COACHING CENTER")
st.markdown("Classes 1st to 12th | Excellence in Education")

# Jab user login na ho, toh sidebar mein Login aur Create Account dikhega
if not st.session_state.logged_in:
    choice = st.sidebar.radio("Navigation", ["Login", "Create Account"], index=0 if st.session_state.page == "Login" else 1)
    st.session_state.page = choice

    if st.session_state.page == "Login":
        st.subheader("🔑 Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login Now"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = "Pooja Mam" if username == "pooja" else username
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    elif st.session_state.page == "Create Account":
        st.subheader("📝 Register New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type='password')
        re_pass = st.text_input("Re-enter Password", type='password')
        
        # Maths Captcha
        st.write(f"**Captcha Check:** Solve `{st.session_state.num1} + {st.session_state.num2}` = ?")
        captcha_ans = st.text_input("Enter Captcha Answer")
        
        if st.button("Register"):
            correct_ans = st.session_state.num1 + st.session_state.num2
            
            if not new_user or not new_pass or not re_pass or not captcha_ans:
                st.warning("Kripya saare fields bharein!")
            elif new_pass != re_pass:
                st.error("Passwords match nahi ho rahe hain!")
            elif captcha_ans.strip() != str(correct_ans):
                st.error("Incorrect Captcha! Sahi answer bharein.")
            elif new_user in st.session_state.users:
                st.error("Yeh Username pehle se maujood hai!")
            else:
                # Save user to session state
                st.session_state.users[new_user] = new_pass
                # Reset Captcha
                st.session_state.num1 = random.randint(1, 9)
                st.session_state.num2 = random.randint(1, 9)
                st.success("Account successfully ban gaya! Ab aap Login kar sakte hain.")
                st.session_state.page = "Login"
                st.rerun()

# Jab user login kar le, tab Student Details & Record Dashboard khulega
else:
    st.sidebar.success(f"Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Login"
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