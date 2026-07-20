import json
import os
from google_auth_oauthlib.flow import Flow

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def main():
    if not os.path.exists('client_secret.json'):
        print("ERROR: I need the client_secret.json first!")
        return

    # Use Flow instead of InstalledAppFlow to manually handle the redirect URL
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/'
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("\n" + "="*50)
    print("USER ACTION REQUIRED:")
    print("="*50)
    print("1. Click this link to authorize with Google:")
    print(auth_url)
    print("\n2. After you sign in, your browser will redirect to a page that says 'This site can't be reached' (localhost). This is NORMAL.")
    print("3. Copy the ENTIRE URL from your browser's address bar (it will start with http://localhost:8080/?state=...)")
    print("="*50 + "\n")

    auth_response = input("Paste the ENTIRE URL here and press Enter: ")

    flow.fetch_token(authorization_response=auth_response.strip())
    credentials = flow.credentials
    
    with open('youtube_token.json', 'w') as f:
        f.write(credentials.to_json())
        
    print("\nSUCCESS! Here is the content for your YOUTUBE_CLIENT_SECRETS:")
    print(credentials.to_json())

if __name__ == '__main__':
    main()
