import streamlit as st

st.set_page_config(page_title="Pooja Sharma Coaching", page_icon="📚", layout="wide")

# Streamlit Secrets se permanent credentials load honge
USERS = st.secrets.get("users", {"pooja": "12345"})

# Session state for login tracking
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

st.title("POOJA SHARMA COACHING CENTER")
st.markdown("Classes 1st to 12th | Excellence in Education")

# Sidebar Navigation (Jaise pehle tha)
choice = st.sidebar.radio("Navigation", ["Login", "Create Account", "Website Home", "Dashboard"])

if choice == "Login":
    st.subheader("🔑 Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login Now"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = "Pooja Mam" if username == "pooja" else username
            st.success(f"Welcome {st.session_state.username}! Login Successful.")
            st.balloons()
        else:
            st.error("Invalid Username or Password")

elif choice == "Create Account":
    st.subheader("📝 Account Information")
    st.info("Aapka permanent login account Streamlit Secrets mein set hai. Aap 'pooja' aur password '12345' use karke seedha Login kar sakte hain. Yeh kabhi delete nahi hoga!")

elif choice == "Website Home":
    st.subheader("🏠 Welcome to Pooja Sharma Coaching Center")
    st.write("Yahan aapki coaching website ka main home page content dikhega.")
    # Aap yahan apna purana home page/HTML templates ya code daal sakte hain

elif choice == "Dashboard":
    if st.session_state.logged_in:
        st.subheader(f"📊 Welcome, {st.session_state.username} - Admin Dashboard")
        st.success("Aapka coaching dashboard successfully load ho gaya hai!")
        # Yahan aapka students, fees, aur classes ka data rahega
    else:
        st.warning("Pehle Login karein tabhi Dashboard khulega!")