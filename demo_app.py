import streamlit as st
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from gmail_utils import authenticate_gmail, scan_inbox

load_dotenv()

st.set_page_config(page_title="UserMaster – Account Scanner Demo")

st.title("📕 UserMaster – Account Scanner Demo")
st.markdown(
    "Welcome to the UserMaster demo. This is a visual simulation of how the app will work once access is approved."
)

st.markdown("### 🔐 Step 1: Enter Your Email")
email = st.text_input("Enter your email address")

agree = st.checkbox("I agree to the [Privacy Policy](https://user-master.com/privacy) and [Terms of Service](https://user-master.com/terms)")

if st.button("🚀 Start Scanning"):
    if not email:
        st.error("Please enter your email address.")
    elif not agree:
        st.error("You must agree to the Privacy Policy and Terms of Service.")
    else:
        st.session_state["email"] = email
        st.session_state["agreed"] = agree
        st.success("✅ Step 1 completed. Please authorize below.")

        auth_params = {
            "client_id": os.getenv("CLIENT_ID"),
            "redirect_uri": os.getenv("REDIRECT_URI"),
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/gmail.readonly",
            "access_type": "offline",
            "prompt": "consent"
        }

        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"
        st.markdown(f"Click the button below to authorize with Google:")
        st.markdown(f"[🔐 Authorize with Google]({auth_url})")

# Handle redirect with `?code=...`
code = st.query_params.get("code")
if code:
    st.success("Authorization successful. Scanning your inbox...")

    try:
        service = authenticate_gmail(code)
        subjects = scan_inbox(service)
        st.markdown("### 📬 Recent Email Subjects:")
        for subject in subjects:
            st.write("•", subject)
    except Exception as e:
        st.error("❌ Failed to get access token from Google.")
        st.exception(e)