import pickle
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import datastore

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def mail_creds():
    """Gets the host, username, and password from Datastore."""
    try:
        # Get auth variables from cloud datastore.
        datastore_client = datastore.Client()
        query = datastore_client.query(kind='GaeEnvSettings')
        env_vars = list(query.fetch())[0]
        return env_vars['MAIL_USERNAME'], env_vars['MAIL_PASSWORD']
    except:
        return os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD')


def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/webserver_gcal_api_client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service
