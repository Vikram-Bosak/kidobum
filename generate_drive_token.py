import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Generates a token.json file to be used as GOOGLE_DRIVE_CREDENTIALS.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('drive_token.json'):
        creds = Credentials.from_authorized_user_file('drive_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secret.json'):
                print("Error: Please download your OAuth 2.0 Client ID JSON file from Google Cloud Console, save it as 'client_secret.json' in this directory, and run this script again.")
                return
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('drive_token.json', 'w') as token:
            token.write(creds.to_json())
    
    print("\n✅ Success! Your 'drive_token.json' has been generated.")
    print("Copy the ENTIRE CONTENTS of 'drive_token.json' and paste it into your GitHub Repository Secret named 'GOOGLE_DRIVE_CREDENTIALS'.")

if __name__ == '__main__':
    main()
