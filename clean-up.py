import os, configparser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# optional to catch errs
from googleapiclient.errors import HttpError

config = configparser.ConfigParser()
config.read('config.ini')

CLIENT_FILE = config['paths']['client_field']
SCOPES = ['https://mail.google.com/']

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
service_gmail = build('gmail', 'v1', credentials=creds)
print(dir(service_gmail))
print("Successfully authenticated and obtained credentials.")


# with open(CLIENT_FILE, 'r') as file:
#     content = file.read()
#     print('HERE: ' + content)