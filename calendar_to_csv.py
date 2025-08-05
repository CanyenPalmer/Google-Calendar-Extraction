import os
import re
import datetime
import pandas as pd
from collections import defaultdict
from urllib.parse import unquote

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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

def extract_phone(text):
    if not text:
        return ''
    match = re.search(r'(\+?\d{1,2}[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    return match.group() if match else ''

def split_location(location_str):
    if not location_str:
        return ('', '', '', '')
    parts = location_str.split(',')
    parts = [p.strip() for p in parts]
    address = parts[0] if len(parts) > 0 else ''
    city = parts[1] if len(parts) > 1 else ''
    state_zip = parts[2] if len(parts) > 2 else ''
    state = state_zip.split()[0] if state_zip else ''
    zip_code = state_zip.split()[1] if len(state_zip.split()) > 1 else ''
    return (address, city, state, zip_code)

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

def process_events(events, filename='calendar_events.xlsx'):
    grouped = defaultdict(list)

    for event in events:
        summary = event.get('summary', 'Untitled Event')
        location = event.get('location', '')
        creator = event.get('creator', {}).get('email', '')
        description = event.get('description', '')

        start = event['start'].get('dateTime', event['start'].get('date'))
        try:
            dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
        except:
            dt = datetime.datetime.strptime(start, "%Y-%m-%d")
        date_str = dt.strftime('%Y-%m-%d')
        time_str = dt.strftime('%I:%M %p') if 'T' in start else 'All Day'

        phone = extract_phone(summary + " " + description)
        key = (summary, location, creator, time_str, phone)
        grouped[key].append(date_str)

    rows = []
    for (summary, location, creator, time, phone), dates in grouped.items():
        address, city, state, zip_code = split_location(location)
        rows.append({
            'Event Name': summary,
            'Event Creator': creator,
            'Event Contact Number': phone,
            'Event Time': time,
            'Event Date(s)': ', '.join(sorted(set(dates))),
            'Address': address,
            'City': city,
            'State': state,
            'ZIP': zip_code
        })

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    print(f"Saved {len(df)} grouped events to {filename}")

if __name__ == '__main__':
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    events = fetch_all_events(service)
    process_events(events)


