import streamlit as st
import pandas as pd
import urllib.parse

# הגדרת הקונפיגורציה של גוגל
CLIENT_ID = "242031868885-13jjtfomjjkb8kqpmu4a05sr3o45bd4h.apps.googleusercontent.com"
REDIRECT_URI = "https://usermaster.streamlit.app"  # כתובת ה-URL של האפליקציה שלך ב-Streamlit
SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
OAUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

# בניית URL ההרשאה
params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": SCOPE,
    "access_type": "offline",
    "include_granted_scopes": "true",
    "prompt": "consent",
}
auth_url = f"{OAUTH_URL}?{urllib.parse.urlencode(params)}"

# ממשק
st.set_page_config(page_title="UserMaster Demo", layout="centered")
st.title("📬 UserMaster - Account Scanner Demo")

st.markdown("""
Welcome to the **UserMaster** demo. This is a visual simulation of how the app will work once access is approved.

Please follow the steps below to simulate an email scan.
""")

# Step 1: Connect Email
st.subheader("🔐 Step 1: Enter Your Email")
email = st.text_input("Enter your email address")
agree = st.checkbox("I agree to the [Privacy Policy](https://user-master.com/privacy) and [Terms of Service](https://user-master.com/terms)")

if st.button("🚀 Start Scanning"):
    if not email and not agree:
        st.warning("Please enter your email and agree to the terms.")
    elif not email:
        st.warning("Please enter your email address to continue.")
    elif not agree:
        st.warning("Please agree to the Privacy Policy and Terms of Service.")
    else:
        st.success("Redirecting to Google for Authorization...")
        js = f"""
        <script>
            window.open("{auth_url}", "_self")
        </script>
        """
        st.components.v1.html(js)