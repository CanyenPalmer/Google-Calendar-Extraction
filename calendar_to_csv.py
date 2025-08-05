import os
import datetime
import pandas as pd

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar read-only access
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_all_events(service, calendar_id='primary'):
    events = []
    page_token = None
    time_min = datetime.datetime(2000, 1, 1).isoformat() + 'Z'
    time_max = datetime.datetime(2100, 1, 1).isoformat() + 'Z'

    while True:
        response = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=2500,
            singleEvents=True,
            orderBy='startTime',
            pageToken=page_token
        ).execute()
        events.extend(response.get('items', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return events

def events_to_csv(events, filename='calendar_events.csv'):
    data = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        data.append({
            'Summary': event.get('summary', ''),
            'Start': start,
            'End': end,
            'Location': event.get('location', ''),
            'Description': event.get('description', ''),
            'Created': event.get('created', ''),
            'Updated': event.get('updated', ''),
            'Event ID': event.get('id', '')
        })
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(events)} events to {filename}")

if __name__ == '__main__':
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    events = fetch_all_events(service)
    events_to_csv(events)

