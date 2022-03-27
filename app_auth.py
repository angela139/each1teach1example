from __future__ import print_function
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()


def connect_firebase():
    # Connect to Firebase
    if os.path.exists('serviceAccount.json'):
        firebase_cred = credentials.Certificate('serviceAccount.json')
    else:
        firebase_cred = credentials.Certificate(
            {
                "type": "service_account",
                "project_id": os.environ['PROJECT_ID'],
                "private_key_id": os.environ['PRIVATE_KEY_ID'],
                "private_key": os.environ['PRIVATE_KEY'].replace('/\\n/g', '\n'),
                "client_email": os.environ['CLIENT_EMAIL'],
                "client_id": os.environ['CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": os.environ['TOKEN_URI'],
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.environ['AUTH_URI']
            }
        )
    if len(firebase_admin._apps) == 0:
        firebase_admin.initialize_app(firebase_cred, {
            'databaseURL': os.environ['DATABASE_URL'],
            'databaseAuthVariableOverride': {
                'uid': os.environ['APP_UID']
            }
        })
    else:
        pass


def connect_google_classroom():
    SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students',
              'https://www.googleapis.com/auth/classroom.rosters', 'https://www.googleapis.com/auth/classroom.courses']
    # Authorize user for Google Classroom API
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file("token.json")
    else:
        creds = Credentials.from_authorized_user_info(
            {"token": os.environ['TOKEN'],
             "refresh_token": os.environ['REFRESH_TOKEN'],
             "token_uri": os.environ['TOKEN_URI'],
             "client_id": os.environ['G_C_CLIENT'],
             "client_secret": os.environ['CLIENT_SECRET'],
             "scopes": SCOPES,
             "expiry": os.environ['EXPIRY']})

    # Create token from new credentials
    '''
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    '''
    return creds
