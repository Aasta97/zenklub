from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import pickle
import os.path


class Calendar:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.credentials_file = 'credentials.json'
        self.service = self.__get_calendar_service()
    
    
    def __get_calendar_service(self):
        credentials = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                credentials = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        service = build('calendar', 'v3', credentials=credentials)
        return service


    def list_calendars(self):
        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars: return 'No calendars found.'
        return calendars
    
    
    def list_events(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        events_result = self.service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events: return 'No upcoming events found.'
        return events
    
    
    def create_event(self, body, calendar_id='primary'):
        return self.service.events().insert(calendarId=calendar_id, body=body).execute()
    
    
    def update_event(self, body, event_id, calendar_id='primary'):
        return self.service.events().update(calendarId=calendar_id, eventId=event_id, body=body).execute()
    
    
    def delete_event(self, event_id, calendar_id='primary'):
       try:
           self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
       except: return 'Failed to delete event'

       return f'Evento deletado: {event_id}'