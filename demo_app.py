import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="UserMaster Demo", layout="centered")

# טקסט פתיחה
st.title("📬 UserMaster - Account Scanner Demo")
st.markdown("Welcome to the **UserMaster** demo. This is a visual simulation of how the app will work once it is approved by Google.")
st.markdown("Please follow the steps below to simulate a Gmail scan.")

# שלב 1 - הכנס כתובת מייל
st.header("🔐 Step 1: Connect Your Gmail")
email = st.text_input("Enter your Gmail address", placeholder="example@gmail.com")

# שלב 2 - סימון הסכמה
agree = st.checkbox("I agree to the [Privacy Policy](https://www.user-master.com/privacy-policy-3) and [Terms of Service](https://www.user-master.com/terms-of-service)")

# כפתור המשך
if email and agree:
    if st.button("🚀 Start Scanning"):
        # שלב 3 - הדמיית סריקה
        with st.spinner("Scanning your inbox for connected accounts..."):
            time.sleep(2)  # סימולציה בזמן סריקה
        st.success("✅ Scan complete!")

        # שלב 4 - הצגת תוצאות מדומות
        st.header("🔎 Connected Accounts Found")
        data = [
            {"Service": "Facebook", "Email": email, "Status": "Active"},
            {"Service": "Netflix", "Email": email, "Status": "Active"},
            {"Service": "Dropbox", "Email": email, "Status": "Inactive"},
        ]
        df = pd.DataFrame(data)
        st.dataframe(df)

        st.info("This is a demo only. No real email scanning has been performed.")

# במידה ולא מולא מייל או לא אושרו תנאים
elif email and not agree:
    st.warning("You must agree to the Privacy Policy and Terms of Service to continue.")
elif agree and not email:
    st.warning("Please enter your Gmail address to continue.")

# תיקון Streamlit שלא מריץ את הקוד לפעמים באחסון חיצוני
if __name__ == "__main__":
    pass  # נדרש לפלטפורמות מסוימות – ניתן להשאיר ריק