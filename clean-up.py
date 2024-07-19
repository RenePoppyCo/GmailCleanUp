"""Delete promotional emails from your Gmail account."""
import os, configparser, json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# authenticate
config = configparser.ConfigParser()
config.read('config.ini')

CLIENT_FILE = config['paths']['client_field']
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

def main():
        
    creds = None

    if os.path.exists('token.json'):
        credits = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: 
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json()) 

    # connect to api service
    try:    
        service_gmail = build('gmail', 'v1', credentials=creds)
        #print(dir(service_gmail))
        print("Successfully authenticated and obtained credentials.")

        # get promotinal emails
        query = 'category:promotions'
        results = service_gmail.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])            

        if not messages:
            print('No promotional emails found...')
            return

        print(f'Found {len(messages)} promotional emails. Deleting...')    

        for message in messages:
            email_id = message['id']
            email_detail = service_gmail.users().messages().get(userId='me', id=email_id, format='full').execute()
            
            headers = email_detail['payload']['headers']
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            print(f'Subject: {subject}')

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()