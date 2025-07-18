import streamlit as st
import os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def exchange_code_for_token(auth_code):
    """Exchange the authorization code for an access token."""
    client_id = st.secrets["CLIENT_ID"]
    client_secret = st.secrets["CLIENT_SECRET"]
    redirect_uri = st.secrets["REDIRECT_URI"]

    print("DEBUG – client_id:", client_id)
    print("DEBUG – client_secret:", client_secret)
    print("DEBUG – redirect_uri:", redirect_uri)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code: {response.text}")

def authenticate_gmail_with_token(access_token):
    """Authenticate with Gmail API using the access token."""
    creds = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def scan_inbox(service, max_results=5):
    """Scan the inbox and return subject lines of recent emails."""
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    subjects = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        subjects.append(subject)
    return subjects