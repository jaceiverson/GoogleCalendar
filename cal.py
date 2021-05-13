import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime as dt
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class Cal():
    def __init__(self,
                 cal_id = None):
        self.service = self.__main_connect()
        self.__all_calendars()
        if cal_id == None:
            self.calId = self.set_default()
        else:
            self.calId = cal_id

    def __all_calendars(self):
        '''
        sets the self.cal_list variable to all the calendars
        that this authentication of google has access to
        
        you can see these by calling self._print_ids()
        '''
        self.cal_list = self.service.calendarList().list().execute()

    def _print_ids(self,data = None):
        '''
        prints the ids of a calendar event, or calendar list
        defaults to printing the calendar list
                
        used when setting up the default calendar
        '''
        if data == None:
            data = self.cal_lsit
        for x in data['items']:
            try:
                print('Name: {}, ID: {}'.format(x['summary'],
                                                x['id']))
            except:
                print('Error with {}'.format(x))
            
    def set_default(self,calId=None):
        '''
        allows you to set a default calendar for this class
        
        this is called automaticly when you init the class
        if the cal_id field is left blank
        '''
        self._print_ids()
        self.calId = input('\nType ID of calendar: ')

    def find_event(self,name):
        '''
        returns an event by event name
        '''
        return self.service.events().list(calendarId = self.calId,
                                          q=name).execute()
            
    def get_event(self,
                  event_id):
        '''
        returns an event by event id
        '''
        return self.service.events().get(calendarId = self.calId,
                                    eventId = event_id
                                    ).execute()
    
    def all_events(self,
                   num_events=250,
                   min_date=dt.date.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                   ):
        '''
        this returns all events on a calendar
        
        defaults to only 100 events, but that can be changed
        up to 2500
        
        returns the dictionary with events in a list
        under the dictionary['items']
        '''
        return self.service.events().list(calendarId=self.calId,
                                     maxResults=num_events,
                                     timeMin = min_date
                                     ).execute()

    def update_event(self,
                     new_event,
                     send_update = 'all'
                     ):
        '''
        accepts the updated dictionary object
        
        uses the 'id' field to update on
        
        option to send updates to invites is default yes
        can change that to 'none', or 'externalOnly'
        
        returns the updated event dictionary
        '''
        return self.service.events().update(calendarId=self.calId,
                                eventId=new_event['id'],
                                body=new_event,
                                sendUpdates = send_update
                                ).execute()

    def __main_connect(self):
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
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        return service
    
if __name__=='__main__':
    print('CALENDAR MODULE')
