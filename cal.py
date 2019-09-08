# [START calendar_quickstart]
from __future__ import print_function
from datetime import date, datetime, time, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from utils import get_week_dates, local_to_iso, iso_to_local

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = 'secrets/token.pickle'
CREDS_PATH = 'secrets/credentials.json'
CAL_INFO_PATH = 'secrets/cal_info.pkl'
CAL_NAME = 'butler'
TZ = 'America/Detroit'

class Calendar(object):
    def __init__(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

        if os.path.exists(CAL_INFO_PATH):
            with open(CAL_INFO_PATH, 'rb') as token:
                self.cal_info = pickle.load(token)
        else:
            self.cal_info = {}

        self._init_calendar()

    def _init_calendar(self):
        if 'id' not in self.cal_info:
            created_calendar = self.service.calendars().insert(body={
                'description': 'Calendar managed by Butler',
                'summary': 'Butler',
                'timeZone': TZ,
            }).execute()
            self.cal_info['id'] = created_calendar['id']

            with open(CAL_INFO_PATH, 'wb') as f:
                pickle.dump(self.cal_info, f)

    def weekly_events(self, calendar_id, index):
        start, end = get_week_dates(index)
        start = datetime.combine(start, datetime.min.time())
        end = datetime.combine(end, time(hour=23, minute=59))

        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=local_to_iso(start),
            timeMax=local_to_iso(end),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = iso_to_local(start)
            print(start, event['summary'])


