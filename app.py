import streamlit as st
import json
import os
import random
import string
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

def generate_captcha():
    return ''.join(random.choice(string.digits) for _ in range(4))

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
if "captcha_code" not in st.session_state:
    st.session_state.captcha_code = generate_captcha()
if "recovered_password" not in st.session_state:
    st.session_state.recovered_password = None
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Initialize persistent users in session state so it never gets lost during runtime
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
            
            cap_col1, cap_col2 = st.columns([4, 1])
            with cap_col1:
                st.markdown(f"<div style='background-color: #1e293b; padding: 12px; border-radius: 8px; text-align: center; font-size: 26px; font-weight: bold; letter-spacing: 8px; color: #38bdf8; border: 1px dashed #6366f1;'>{st.session_state.captcha_code}</div>", unsafe_allow_html=True)
            with cap_col2:
                if st.button("🔄", help="Refresh Captcha"):
                    st.session_state.captcha_code = generate_captcha()
                    st.rerun()
            
            user_captcha = st.text_input("Enter 4-Digit Code Shown Above", key="r_captcha")
            
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
                    st.session_state.users_db = users
                    save_users(users)
                    st.success("Account successfully ban gaya! Ab aap Login kar sakte hain.")
                    st.session_state.captcha_code = generate_captcha()
                    st.session_state.page_choice = "🔐 Login"
                    st.rerun()

else:
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
    
    with st.expander("📝 Compact Student Data Feed Form", expanded=True):
        edit_data = {}
        is_editing = False
        if st.session_state.edit_index is not None and st.session_state.edit_index < len(students_db):
            edit_data = students_db[st.session_state.edit_index]
            is_editing = True
            st.info(f"Editing Student: {edit_data.get('Student Name', '')}")

        with st.form("student_form", clear_on_submit=False):
            fc1, fc2, fc3 = st.columns(3)
            
            with fc1:
                s_name = st.text_input("Student Name *", value=edit_data.get("Student Name", ""))
                class_options = [f"{i}th Class" if i > 3 else (f"{i}st Class" if i==1 else (f"{i}nd Class" if i==2 else f"{i}rd Class")) for i in range(1, 13)]
                default_class_idx = class_options.index(edit_data.get("Class")) if edit_data.get("Class") in class_options else 0
                s_class = st.selectbox("Class *", class_options, index=default_class_idx)
                s_school = st.text_input("School Name *", value=edit_data.get("School", ""))
                s_subject = st.text_input("Subject *", value=edit_data.get("Subject", ""))

            with fc2:
                s_phone = st.text_input("Student Phone Number", value=edit_data.get("Phone", ""))
                m_name = st.text_input("Mother Name *", value=edit_data.get("Mother Name", ""))
                m_phone = st.text_input("Mother Contact No *", value=edit_data.get("Mother Contact", ""))
                f_name = st.text_input("Father Name", value=edit_data.get("Father Name", ""))

            with fc3:
                f_phone = st.text_input("Father Contact No", value=edit_data.get("Father Contact", ""))
                fee_status = st.text_input("Fee Status / Amount *", value=edit_data.get("Fee Status", ""))
                
                default_date = datetime.date.today()
                if edit_data.get("Fee Date"):
                    try:
                        default_date = datetime.datetime.strptime(edit_data.get("Fee Date"), "%Y-%m-%d").date()
                    except:
                        pass
                fee_date = st.date_input("Fee Date *", value=default_date)
                s_address = st.text_input("Address *", value=edit_data.get("Address", ""))

            btn_label = "Update Student Data" if is_editing else "Save Student Data"
            
            if is_editing:
                btn_c1, btn_c2 = st.columns([3, 1])
                with btn_c1:
                    submitted = st.form_submit_button(btn_label, type="primary", use_container_width=True)
                with btn_c2:
                    cancel_edit = st.form_submit_button("❌ Cancel Edit", use_container_width=True)
            else:
                submitted = st.form_submit_button(btn_label, type="primary", use_container_width=True)
                cancel_edit = False

            if cancel_edit:
                st.session_state.edit_index = None
                st.rerun()

            if submitted:
                missing_fields = []
                if not s_name.strip():
                    missing_fields.append("Student Name")
                if not s_school.strip():
                    missing_fields.append("School Name")
                if not s_subject.strip():
                    missing_fields.append("Subject")
                if not m_name.strip():
                    missing_fields.append("Mother Name")
                if not m_phone.strip():
                    missing_fields.append("Mother Contact No")
                if not fee_status.strip():
                    missing_fields.append("Fee Status / Amount")
                if not fee_date:
                    missing_fields.append("Fee Date")
                if not s_address.strip():
                    missing_fields.append("Address")
                if not s_phone.strip() and not m_phone.strip() and not f_phone.strip():
                    missing_fields.append("At least one Phone Number")
                
                if missing_fields:
                    st.error(f"⚠️ Mandatory fields are missing! Please fill in: **{', '.join(missing_fields)}**")
                else:
                    new_student = {
                        "Student Name": s_name.strip(),
                        "Class": s_class,
                        "School": s_school.strip(),
                        "Subject": s_subject.strip(),
                        "Phone": s_phone.strip() if s_phone.strip() else (m_phone.strip() if m_phone.strip() else f_phone.strip()),
                        "Mother Name": m_name.strip(),
                        "Mother Contact": m_phone.strip(),
                        "Father Name": f_name.strip(),
                        "Father Contact": f_phone.strip(),
                        "Address": s_address.strip(),
                        "Fee Status": fee_status.strip(),
                        "Fee Date": str(fee_date)
                    }
                    
                    if is_editing:
                        students_db[st.session_state.edit_index] = new_student
                        st.session_state.edit_index = None
                        st.success("Student data updated successfully!")
                    else:
                        students_db.append(new_student)
                        st.success("Student data saved successfully!")
                    
                    save_students(students_db)
                    st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Students Details")
    
    if students_db and isinstance(students_db, list) and len(students_db) > 0:
        for idx, student in enumerate(students_db):
            with st.expander(f"👤 {student.get('Student Name', 'N/A')} — {student.get('Class', 'N/A')} ({student.get('School', 'N/A')})"):
                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1:
                    st.write(f"**Subject:** {student.get('Subject', '-')}")
                    st.write(f"**Phone:** {student.get('Phone', '-')}")
                    st.write(f"**Address:** {student.get('Address', '-')}")
                with col_d2:
                    st.write(f"**Mother Name:** {student.get('Mother Name', '-')}")
                    st.write(f"**Mother Contact:** {student.get('Mother Contact', '-')}")
                    st.write(f"**Father Name:** {student.get('Father Name', '-')}")
                with col_d3:
                    st.write(f"**Father Contact:** {student.get('Father Contact', '-')}")
                    st.write(f"**Fee Status:** {student.get('Fee Status', '-')}")
                    st.write(f"**Fee Date:** {student.get('Fee Date', '-')}")
                
                b1, b2, _ = st.columns([1, 1, 4])
                with b1:
                    if st.button("✏️ Edit", key=f"edit_{idx}"):
                        st.session_state.edit_index = idx
                        st.rerun()
                with b2:
                    if st.button("🗑️ Delete", key=f"del_{idx}"):
                        students_db.pop(idx)
                        save_students(students_db)
                        if st.session_state.edit_index == idx:
                            st.session_state.edit_index = None
                        st.success("Student data deleted successfully!")
                        st.rerun()
    else:
        st.info("No student data has been added yet.")