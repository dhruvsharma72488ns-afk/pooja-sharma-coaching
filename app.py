import streamlit as st
import random
import datetime

st.set_page_config(
    page_title="Pooja Sharma Coaching Center", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State securely
if "users" not in st.session_state:
    st.session_state.users = {"pooja": "12345"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Login"

if "students" not in st.session_state:
    st.session_state.students = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Captcha Numbers
if "num1" not in st.session_state or "num2" not in st.session_state:
    st.session_state.num1 = random.randint(1, 9)
    st.session_state.num2 = random.randint(1, 9)

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
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
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
            with st.form("register_form_safe"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("Password", type="password")
                re_pass = st.text_input("Re-enter Password", type="password")
                
                st.write(f"**Captcha:** `{st.session_state.num1} + {st.session_state.num2}` kitna hota hai?")
                captcha_ans = st.text_input("Captcha Answer")
                
                register_btn = st.form_submit_button("Register Account", type="primary")
                
                if register_btn:
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
                        st.success("✅ Account ban gaya! Ab aap Login kar sakte hain.")
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
    fee_status_options = ["Paid", "Pending"]

    # --- EDIT MODE ---
    if st.session_state.edit_index is not None:
        idx = st.session_state.edit_index
        student = st.session_state.students[idx]
        st.subheader(f"✏️ Edit Student Record: {student['Student Name']}")
        
        with st.form("edit_student_form"):
            st.markdown("### 🎓 Student & Parents Details")
            c1, c2 = st.columns(2)
            with c1:
                e_name = st.text_input("Student Name", value=student["Student Name"])
                e_class = st.selectbox("Class", class_options, index=class_options.index(student["Class"]))
                e_phone = st.text_input("Student Phone Number", value=student["Student Phone"])
                e_mname = st.text_input("Mother's Name", value=student["Mother Name"])
                e_mphone = st.text_input("Mother's Contact Number", value=student["Mother Contact"])
            with c2:
                e_fname = st.text_input("Father's Name", value=student["Father Name"])
                e_fphone = st.text_input("Father's Contact Number", value=student["Father Contact"])
                e_address = st.text_input("Address (Chhota box)", value=student["Address"])

            st.markdown("### 💰 Fee Structure & Calendar")
            c3, c4 = st.columns(2)
            with c3:
                e_fee_total = st.number_input("Total Fee Structure (₹)", min_value=0, value=int(student["Total Fees"]))
                e_fee_paid = st.number_input("Fees Submitted (₹)", min_value=0, value=int(student["Paid Fees"]))
            with c4:
                e_fee_date = st.date_input("Fee Submission Date (Calendar)", value=student["Fee Date"])
                e_fee_status = st.selectbox("Fee Status", fee_status_options, index=fee_status_options.index(student["Fee Status"]))

            col_save, col_cancel = st.columns(2)
            with col_save:
                update_btn = st.form_submit_button("💾 Update Record", type="primary")
            with col_cancel:
                cancel_btn = st.form_submit_button("❌ Cancel")

            if update_btn:
                st.session_state.students[idx] = {
                    "Student Name": e_name, "Class": e_class, "Student Phone": e_phone,
                    "Mother Name": e_mname, "Mother Contact": e_mphone,
                    "Father Name": e_fname, "Father Contact": e_fphone,
                    "Address": e_address, "Total Fees": e_fee_total, "Paid Fees": e_fee_paid,
                    "Fee Date": e_fee_date, "Fee Status": e_fee_status
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
            st.markdown("### 🎓 Student & Parents Details")
            c1, c2 = st.columns(2)
            with c1:
                s_name = st.text_input("Student Name *")
                s_class = st.selectbox("Select Class *", class_options)
                s_phone = st.text_input("Student Phone Number")
                m_name = st.text_input("Mother's Name")
                m_phone = st.text_input("Mother's Contact Number")
            with c2:
                f_name = st.text_input("Father's Name *")
                f_phone = st.text_input("Father's Contact Number *")
                address = st.text_input("Address (Chhota box)")

            st.markdown("### 💰 Fee Structure & Calendar")
            c3, c4 = st.columns(2)
            with c3:
                total_fees = st.number_input("Total Fee Structure (₹)", min_value=0, step=100)
                paid_fees = st.number_input("Fees Submitted (₹)", min_value=0, step=100)
            with c4:
                fee_date = st.date_input("Fee Submission Date (Calendar)", value=datetime.date.today())
                fee_status = st.selectbox("Fee Status", fee_status_options)

            submit_btn = st.form_submit_button("✅ Submit Student Record", type="primary")

            if submit_btn:
                if not s_name or not f_name:
                    st.error("⚠️ Student Name aur Father's Name bharna zaroori hai!")
                else:
                    st.session_state.students.append({
                        "Student Name": s_name, "Class": s_class, "Student Phone": s_phone,
                        "Mother Name": m_name, "Mother Contact": m_phone,
                        "Father Name": f_name, "Father Contact": f_phone,
                        "Address": address, "Total Fees": total_fees, "Paid Fees": paid_fees,
                        "Fee Date": fee_date, "Fee Status": fee_status
                    })
                    st.success(f"🎉 {s_name} ka record successfully save ho gaya!")

    st.markdown("---")
    
    # --- DISPLAY ALL RECORDS ---
    st.subheader(f"📋 All Registered Students ({len(st.session_state.students)})")
    
    if len(st.session_state.students) == 0:
        st.info("Abhi tak koi student record add nahi kiya gaya hai.")
    else:
        for i, stu in enumerate(st.session_state.students):
            with st.expander(f"🎓 {stu['Student Name']} | {stu['Class']} | Fee Status: {stu['Fee Status']} (Date: {stu['Fee Date']})"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Student Name:** {stu['Student Name']}")
                    st.write(f"**Class:** {stu['Class']}")
                    st.write(f"**Student Phone:** {stu['Student Phone']}")
                    st.write(f"**Mother's Name:** {stu['Mother Name']} | **Contact:** {stu['Mother Contact']}")
                    st.write(f"**Father's Name:** {stu['Father Name']} | **Contact:** {stu['Father Contact']}")
                with col_b:
                    st.write(f"**Total Fees:** ₹{stu['Total Fees']}")
                    st.write(f"**Fees Paid:** ₹{stu['Paid Fees']}")
                    st.write(f"**Fee Submission Date:** {stu['Fee Date']}")
                    st.write(f"**Fee Status:** {stu['Fee Status']}")
                    st.write(f"**Address:** {stu['Address']}")
                    
                    if st.button(f"✏️ Edit {stu['Student Name']}", key=f"edit_{i}"):
                        st.session_state.edit_index = i
                        st.rerun()