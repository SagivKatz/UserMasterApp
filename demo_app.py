import streamlit as st
import pandas as pd

# Title and header
st.set_page_config(page_title="UserMaster Demo", layout="centered")
st.title("📬 UserMaster - Account Scanner Demo")

st.markdown("""
Welcome to the **UserMaster** demo. This is a visual simulation of how the app will work once access is approved.

Please follow the steps below to simulate an email scan.
""")

# Step 1: Connect Email
st.subheader("🔐 Step 1: Enter Your Email")
email = st.text_input("Enter your email address")

# Terms and conditions
agree = st.checkbox("I agree to the [Privacy Policy](https://user-master.com/privacy) and [Terms of Service](https://user-master.com/terms)")

# Simulate scan
if st.button("🚀 Start Scanning"):
    if not agree and not email:
        st.warning("Please enter your email and agree to the terms.")
    elif not agree:
        st.warning("Please agree to the Privacy Policy and Terms of Service.")
    elif not email:
        st.warning("Please enter your email address to continue.")
    else:
        st.success("✅ Scan complete!")

        # Simulated results
        data = [
            {"Service": "Facebook", "Email": email, "Status": "Active"},
            {"Service": "Netflix", "Email": email, "Status": "Active"},
            {"Service": "Dropbox", "Email": email, "Status": "Inactive"},
        ]
        df = pd.DataFrame(data)
        st.subheader("🔍 Connected Accounts Found")
        st.dataframe(df, use_container_width=True)
        st.info("This is a demo only. No real email scanning has been performed.")