import streamlit as st
from gmail_utils import exchange_code_for_token, authenticate_gmail_with_token, scan_inbox
from dotenv import load_dotenv
import os
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

st.set_page_config(page_title="UserMaster – Account Scanner Demo", page_icon="📕", layout="centered")

# Apply basic CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("📕 UserMaster – Account Scanner Demo")
st.markdown("""
Welcome to the UserMaster demo. This is a visual simulation of how the app will work once access is approved.
""")

# Step 1 – Enter Email
st.subheader("🔐 Step 1: Enter Your Email")

email = st.text_input("Enter your email address")

agree = st.checkbox("I agree to the [Privacy Policy](https://user-master.com/privacy) and [Terms of Service](https://user-master.com/terms)")

# Build OAuth URL
def build_auth_url():
    client_id = os.getenv("CLIENT_ID")
    redirect_uri = os.getenv("REDIRECT_URI")
    scope = "https://www.googleapis.com/auth/gmail.readonly"
    response_type = "code"
    access_type = "offline"
    prompt = "consent"

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type={response_type}"
        f"&scope={scope}"
        f"&access_type={access_type}"
        f"&prompt={prompt}"
    )
    return auth_url

# Step 2 – OAuth redirect
if email and agree:
    if st.button("🚀 Start Scanning"):
        st.warning("Click the button below to authorize with Google:")
        auth_url = build_auth_url()
        st.markdown(f'<a href="{auth_url}" target="_blank"><button>🔐 Authorize with Google</button></a>', unsafe_allow_html=True)

# Step 3 – Check for ?code= in URL (after redirect)
query_params = st.query_params
auth_code = query_params.get("code", [None])[0]

if auth_code:
    st.success("✅ Authorization successful. Scanning your inbox...")
    try:
        token_data = exchange_code_for_token(auth_code)
        access_token = token_data.get("access_token")

        if access_token:
            service = authenticate_gmail_with_token(access_token)
            subjects = scan_inbox(service)

            st.write("📧 Recent email subjects:")
            for i, subject in enumerate(subjects, 1):
                st.write(f"{i}. {subject}")
        else:
            st.error("❌ Failed to get access token from Google.")
    except Exception as e:
        st.error(f"An error occurred: {e}")