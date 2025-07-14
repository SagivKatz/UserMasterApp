import streamlit as st
import urllib.parse
import os
import requests
from dotenv import load_dotenv
from gmail_utils import scan_inbox  # פונקציית סריקה מתוך gmail_utils

load_dotenv()

# ============================
# הגדרות קבועות ל-OAuth
# ============================
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

# ============================
# פונקציה לבניית קישור הרשאה
# ============================
def build_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    return AUTH_URL + "?" + urllib.parse.urlencode(params)

# ============================
# פונקציה להמרת הקוד ל-token
# ============================
def exchange_code_for_token(code):
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json()

# ============================
# בניית שירות Gmail מה-token
# ============================
def build_service(access_token):
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials

    creds = Credentials(
        token=access_token,
        refresh_token=None,
        token_uri=TOKEN_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=[SCOPE]
    )
    return build('gmail', 'v1', credentials=creds)

# ============================
# ממשק ראשי
# ============================
st.set_page_config(page_title="UserMaster Demo", page_icon="📕")
st.title("📕 UserMaster – Account Scanner Demo")
st.write("Welcome to the UserMaster demo. This is a visual simulation of how the app will work once access is approved.")

# בדיקה אם המשתמש חזר עם הקוד
query_params = st.query_params
if "code" in query_params:
    code = query_params["code"][0]
    st.success("✅ Authorization successful. Scanning your inbox...")

    token_data = exchange_code_for_token(code)
    access_token = token_data.get("access_token")

    if not access_token:
        st.error("❌ Failed to get access token from Google.")
    else:
        service = build_service(access_token)
        subjects = scan_inbox(service, max_results=10)
        st.markdown("### ✉️ Recent Email Subjects:")
        for i, subject in enumerate(subjects, 1):
            st.write(f"{i}. {subject}")

# אין עדיין code – מציגים טופס התחלה
else:
    st.markdown("### 🔐 Step 1: Enter Your Email")
    email = st.text_input("Enter your email address")

    agree = st.checkbox("I agree to the [Privacy Policy](https://user-master.com/privacy) and [Terms of Service](https://user-master.com/terms)", value=False)

    if st.button("🚀 Start Scanning") and agree and email:
        auth_url = build_auth_url()
        js = f"""
        <script>
            window.open("{auth_url}", "_self");
        </script>
        """
        st.components.v1.html(js, height=0)

    # 🔴 הסרת הקישור הידני – לא צריך אותו:
    # st.markdown(f"[Click here to authorize with Google]({build_auth_url()})")