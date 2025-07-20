import os
import requests
import urllib.parse

def exchange_code_for_token(auth_code):
    """
    Exchange the authorization code for an access token.
    """

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")

    print("DEBUG – client_id length:", len(client_id))
    print("DEBUG – client_secret length:", len(client_secret))
    print("DEBUG – redirect_uri:", redirect_uri)

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

    encoded_data = urllib.parse.urlencode(data)

    response = requests.post(token_url, data=encoded_data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code: {response.text}")