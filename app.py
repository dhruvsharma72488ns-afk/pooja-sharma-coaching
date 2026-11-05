import streamlit as st

st.set_page_config(page_title="Pooja Sharma Coaching", page_icon="📚")

st.title("POOJA SHARMA COACHING CENTER")
st.markdown("Classes 1st to 12th | Excellence in Education")

# Streamlit Secrets se permanent users load honge jo kabhi delete nahi honge
USERS = st.secrets.get("users", {"pooja": "12345"})

choice = st.sidebar.radio("Navigation", ["Login", "Create Account"])

if choice == "Login":
    st.subheader("🔑 Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login Now"):
        if username in USERS and USERS[username] == password:
            st.success(f"Welcome {username}! Login Successful.")
            # Yahan aapka aage ka coaching dashboard/portal code aayega
        else:
            st.error("Invalid Username or Password")

elif choice == "Create Account":
    st.info("Permanent login ke liye aapka account Streamlit Secrets mein set hai. Aap 'pooja' aur password '12345' se seedha Login kar sakte hain.")