import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def exchange_code_for_token(auth_code):
    """Exchange the authorization code for an access token."""
    import os

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
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


def scan_inbox(service):
    """Scan inbox and return recent email subjects."""
    try:
        result = service.users().messages().list(userId='me', maxResults=5).execute()
        messages = result.get('messages', [])
        subjects = []

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject']).execute()
            headers = msg_data['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "(No Subject)")
            subjects.append(subject)

        return subjects

    except Exception as e:
        return [f"Error scanning inbox: {e}"]