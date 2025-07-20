import os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def exchange_code_for_token(auth_code):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")

    # Debug output
    print("client_id length:", len(client_id))
    print("client_secret length:", len(client_secret))
    print("redirect_uri:", redirect_uri)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code: {response.text}")

def authenticate_gmail_with_token(access_token):
    creds = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def scan_inbox(service, max_results=5):
    try:
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        subjects = []

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data['payload'].get('headers', [])
            for header in headers:
                if header['name'].lower() == 'subject':
                    subjects.append(header['value'])
        return subjects
    except Exception as e:
        raise Exception(f"Failed to scan inbox: {e}")