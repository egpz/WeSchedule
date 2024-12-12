from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta

import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """
    Authenticates the user with the Google Calendar API and returns credentials.
    """
    creds = None
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials, log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_calendar_event(creds, event_name, start_time, end_time, attendees, date):
    """
    Creates a Google Calendar event with a specific date.
    :param creds: Google API credentials.
    :param event_name: Name of the event.
    :param start_time: Event start time (24-hour format, e.g., "13:00").
    :param end_time: Event end time (24-hour format, e.g., "14:00").
    :param attendees: List of attendee email addresses.
    :param date: Specific date for the event (format: YYYY-MM-DD).
    """
    service = build('calendar', 'v3', credentials=creds)

    # Parse the date and time into datetime objects
    start_datetime = datetime.strptime(f"{date} {start_time}", '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(f"{date} {end_time}", '%Y-%m-%d %H:%M')

    # Create the event
    event = {
        'summary': event_name,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'America/New_York',
        },
        'attendees': [{'email': email.strip()} for email in attendees],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
    