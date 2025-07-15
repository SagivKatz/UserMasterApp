import os
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail(auth_code):
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': auth_code,
        'client_id': os.getenv("CLIENT_ID"),
        'client_secret': os.getenv("CLIENT_SECRET"),
        'redirect_uri': os.getenv("REDIRECT_URI"),
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")
    
    tokens = response.json()
    access_token = tokens.get('access_token')

    from google.oauth2.credentials import Credentials
    creds = Credentials(token=access_token)

    service = build('gmail', 'v1', credentials=creds)
    return service