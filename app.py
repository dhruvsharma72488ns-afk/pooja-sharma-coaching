import streamlit as st
import random
import datetime
import pandas as pd

st.set_page_config(
    page_title="Pooja Sharma Coaching Center", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Permanent Login Credentials + Session Users
if "users" not in st.session_state:
    st.session_state.users = st.secrets.get("users", {"pooja": "12345"})

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Login"

# Student Records Storage
if "students" not in st.session_state:
    st.session_state.students = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Captcha Setup
if "num1" not in st.session_state or "num2" not in st.session_state:
    st.session_state.num1 = random.randint(1, 9)
    st.session_state.num2 = random.randint(1, 9)

# Header
st.title("📚 POOJA SHARMA COACHING CENTER")
st.markdown("**Classes 1st to 12th | Excellence in Education**")
st.markdown("---")

# ==========================================
# 1. LOGIN & CREATE ACCOUNT SECTION
# ==========================================
if not st.session_state.logged_in:
    choice = st.sidebar.radio(
        "Navigation", 
        ["Login", "Create Account"], 
        index=0 if st.session_state.page == "Login" else 1
    )
    st.session_state.page = choice

    if st.session_state.page == "Login":
        st.subheader("🔑 Login to Your Account")
        col1, _ = st.columns([1, 1])
        with col1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login Now", type="primary"):
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = "Pooja Mam" if username.lower() == "pooja" else username
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password")

    elif st.session_state.page == "Create Account":
        st.subheader("📝 Create New Account")
        col1, _ = st.columns([1, 1])
        with col1:
            new_user = st.text_input("New Username")
            new_pass = st.text_input("Password", type="password")
            re_pass = st.text_input("Re-enter Password", type="password")
            
            st.write(f"**Captcha:** `{st.session_state.num1} + {st.session_state.num2}` kitna hota hai?")
            captcha_ans = st.text_input("Captcha Answer")
            
            if st.button("Register Account", type="primary"):
                correct_ans = st.session_state.num1 + st.session_state.num2
                if not new_user or not new_pass or not re_pass or not captcha_ans:
                    st.warning("⚠️ Kripya saare fields bharein!")
                elif new_pass != re_pass:
                    st.error("❌ Password aur Re-password match nahi ho rahe!")
                elif captcha_ans.strip() != str(correct_ans):
                    st.error("❌ Galat Captcha! Dobara try karein.")
                elif new_user in st.session_state.users:
                    st.error("⚠️ Yeh Username pehle se bana hua hai!")
                else:
                    st.session_state.users[new_user] = new_pass
                    st.session_state.num1 = random.randint(1, 9)
                    st.session_state.num2 = random.randint(1, 9)
                    st.success("✅ Account ban gaya! Ab Login karein.")
                    st.session_state.page = "Login"
                    st.rerun()

# ==========================================
# 2. MAIN PORTAL (AFTER LOGIN)
# ==========================================
else:
    st.sidebar.success(f"👋 Welcome, {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.rerun()

    st.success(f"### 🎉 Welcome {st.session_state.username}!")

    class_options = [
        "1st Class", "2nd Class", "3rd Class", "4th Class", "5th Class",
        "6th Class", "7th Class", "8th Class", "9th Class", "10th Class",
        "11th Class", "12th Class"
    ]

    # --- EDIT MODE CHECK ---
    if st.session_state.edit_index is not None:
        idx = st.session_state.edit_index
        student = st.session_state.students[idx]
        st.subheader(f"✏️ Edit Student Record: {student['Student Name']}")
        
        with st.form("edit_student_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                e_name = st.text_input("Student Name", value=student["Student Name"])
                e_class = st.selectbox("Class", class_options, index=class_options.index(student["Class"]))
                e_phone = st.text_input("Student Phone Number", value=student["Student Phone"])
            with c2:
                e_fname = st.text_input("Father's Name", value=student["Father Name"])
                e_fphone = st.text_input("Father's Contact Number", value=student["Father Contact"])
                e_mname = st.text_input("Mother's Name", value=student["Mother Name"])
            with c3:
                e_mphone = st.text_input("Mother's Contact Number", value=student["Mother Contact"])
                e_fee_total = st.number_input("Total Fees (₹)", min_value=0, value=int(student["Total Fees"]))
                e_fee_paid = st.number_input("Fees Paid (₹)", min_value=0, value=int(student["Paid Fees"]))
            
            c4, c5 = st.columns(2)
            with c4:
                e_address = st.text_area("Student Address", value=student["Address"])
            with c5:
                e_fee_date = st.date_input("Fee Submission Date", value=student["Fee Date"])
                e_fee_status = st.selectbox("Fee Status", ["Paid", "Partial", "Pending"], index=["Paid", "Partial", "Pending"].index(student["Fee Status"]))

            col_save, col_cancel = st.columns(2)
            with col_save:
                update_btn = st.form_submit_button("💾 Update Record", type="primary")
            with col_cancel:
                cancel_btn = st.form_submit_button("❌ Cancel")

            if update_btn:
                st.session_state.students[idx] = {
                    "Student Name": e_name,
                    "Class": e_class,
                    "Student Phone": e_phone,
                    "Father Name": e_fname,
                    "Father Contact": e_fphone,
                    "Mother Name": e_mname,
                    "Mother Contact": e_mphone,
                    "Address": e_address,
                    "Total Fees": e_fee_total,
                    "Paid Fees": e_fee_paid,
                    "Fee Date": e_fee_date,
                    "Fee Status": e_fee_status
                }
                st.session_state.edit_index = None
                st.success("✅ Record successfully update ho gaya!")
                st.rerun()
            if cancel_btn:
                st.session_state.edit_index = None
                st.rerun()

    # --- ADD NEW STUDENT FORM ---
    else:
        st.subheader("➕ Add New Student Details & Fee Record")
        with st.form("add_student_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                s_name = st.text_input("Student Name *")
                s_class = st.selectbox("Select Class *", class_options)
                s_phone = st.text_input("Student Phone Number")
            with c2:
                f_name = st.text_input("Father's Name *")
                f_phone = st.text_input("Father's Contact Number *")
                m_name = st.text_input("Mother's Name")
            with c3:
                m_phone = st.text_input("Mother's Contact Number")
                total_fees = st.number_input("Total Fee Structure (₹)", min_value=0, step=100)
                paid_fees = st.number_input("Fees Submitted (₹)", min_value=0, step=100)
            
            c4, c5 = st.columns(2)
            with c4:
                address = st.text_area("Full Address")
            with c5:
                fee_date = st.date_input("Fee Submission Date (Calendar)", value=datetime.date.today())
                fee_status = st.selectbox("Fee Status", ["Paid", "Partial", "Pending"])

            submit_btn = st.form_submit_button("✅ Submit Student Record", type="primary")

            if submit_btn:
                if not s_name or not f_name:
                    st.error("⚠️ Student Name aur Father's Name bharna zaroori hai!")
                else:
                    st.session_state.students.append({
                        "Student Name": s_name,
                        "Class": s_class,
                        "Student Phone": s_phone,
                        "Father Name": f_name,
                        "Father Contact": f_phone,
                        "Mother Name": m_name,
                        "Mother Contact": m_phone,
                        "Address": address,
                        "Total Fees": total_fees,
                        "Paid Fees": paid_fees,
                        "Fee Date": fee_date,
                        "Fee Status": fee_status
                    })
                    st.success(f"🎉 {s_name} ka record successfully save ho gaya!")

    st.markdown("---")
    
    # --- DISPLAY ALL RECORDS WITH EDIT OPTION ---
    st.subheader(f"📋 All Registered Students ({len(st.session_state.students)})")
    
    if len(st.session_state.students) == 0:
        st.info("Abhi tak koi student record add nahi kiya gaya hai. Upar form bharkar add karein.")
    else:
        for i, stu in enumerate(st.session_state.students):
            with st.expander(f"🎓 {stu['Student Name']} | {stu['Class']} | Fee Status: {stu['Fee Status']} (Date: {stu['Fee Date']})"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.write(f"**Student Name:** {stu['Student Name']}")
                    st.write(f"**Class:** {stu['Class']}")
                    st.write(f"**Student Phone:** {stu['Student Phone']}")
                    st.write(f"**Address:** {stu['Address']}")
                with col_b:
                    st.write(f"**Father's Name:** {stu['Father Name']}")
                    st.write(f"**Father's Contact:** {stu['Father Contact']}")
                    st.write(f"**Mother's Name:** {stu['Mother Name']}")
                    st.write(f"**Mother's Contact:** {stu['Mother Contact']}")
                with col_c:
                    st.write(f"**Total Fees:** ₹{stu['Total Fees']}")
                    st.write(f"**Fees Paid:** ₹{stu['Paid Fees']}")
                    st.write(f"**Fee Date:** {stu['Fee Date']}")
                    st.write(f"**Status:** {stu['Fee Status']}")
                    
                    if st.button(f"✏️ Edit {stu['Student Name']}", key=f"edit_{i}"):
                        st.session_state.edit_index = i
                        st.rerun()