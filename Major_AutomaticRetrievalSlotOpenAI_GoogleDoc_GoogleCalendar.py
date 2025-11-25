import os
import sys
import warnings
import constants
import time

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.llms import openai
from langchain_community.chat_models import ChatOpenAI
import os
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# SCOPES = ['https://www.googleapis.com/auth/calendar']
#Defining scopes for both Google doc API and Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/documents","https://www.googleapis.com/auth/calendar"]

# Defining the document ID of the google doc to locate the google document
documentId='1v7kkpOZaE3ACQLSEuN1sgNDjeHcSJ0HWpGhmvVu3bEA'

main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

output_folder = os.path.join(main_folder,'demo_AutomaticSlotRetrieval')
output_file = 'autoSlotRetrievalGoogleDoc.txt'

warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = constants.APIKEY

def handling_credentials(SCOPES):
    credentials = None
    if os.path.exists("token3.json"):
        credentials = Credentials.from_authorized_user_file("token3.json",SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_latest.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token3.json',"w") as token:
            token.write(credentials.to_json())
    print(credentials)
    return credentials

def clear_google_doc(service_docs):
    '''
    Clearing the google document content initially and then writing the content of available time slots in the Google document
    '''
    document = service_docs.documents().get(documentId=documentId).execute()
    content = document.get('body', {}).get('content', [])

    if not content:
        print("The google doc file was initially empty.")
        return

    last_segment = content[-1]
    start_index = 1  
    end_index = last_segment['endIndex']  

    if last_segment['paragraph']['elements'][-1].get('textRun'):
        end_index = end_index - 1  

    requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': start_index,
                    'endIndex': end_index
                }
            }
        }
    ]
    service_docs.documents().batchUpdate(documentId=documentId, body={'requests': requests}).execute()


def AutomaticEventRetrievalToDoc():
    creds = handling_credentials(SCOPES)

    try:
        service_calendar = build('calendar', 'v3', credentials=creds)
        date_time_now = dt.datetime.now()
        end_day_retrieveEvents = date_time_now + dt.timedelta(days=1)
        end_day_retrieveEvents = dt.datetime.combine(end_day_retrieveEvents.date(), dt.time.min)

        print("Checking availability from", date_time_now.isoformat(), "to", end_day_retrieveEvents.isoformat())

        eventResult = service_calendar.events().list(
            calendarId='vishakharamteke63@gmail.com',
            timeMin=date_time_now.isoformat() + 'Z',
            timeMax=end_day_retrieveEvents.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        # print('Event Result is::::', eventResult)

        events = eventResult.get('items', [])

        # Set to store already booked events.
        events_booked = set()

        # Extracting booked time slots from events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            event_start_time = dt.datetime.fromisoformat(start[:-1])
            event_end_time = dt.datetime.fromisoformat(end[:-1])

            while event_start_time < event_end_time:
                events_booked.add(event_start_time)
                event_start_time = event_start_time + dt.timedelta(hours=1)

        available_slots = []

        # Adjusting start time to the next immediate hour slot after the current time
        current_time = date_time_now.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)
        while current_time < end_day_retrieveEvents:
            if current_time not in events_booked:  # Checking if the slot is not booked
                slot_end_time = current_time + dt.timedelta(hours=1)
                if slot_end_time > end_day_retrieveEvents:
                    break
                slot_str = current_time.strftime("%A %Y-%m-%dT%H:%M:%S") + ' to ' + slot_end_time.strftime("%Y-%m-%dT%H:%M:%S")
                available_slots.append(slot_str)
            current_time = current_time + dt.timedelta(hours=1)

        # Printing the available time slots in the console
        # print("Available time slots:")
        # for slot in available_slots:
        #     print(slot)

        service_docs = build('docs', 'v1', credentials=creds)
        clear_google_doc(service_docs)

        if available_slots:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': 'I am Vishakha Ramteke and I study at Sacramento State University in California' + '\nBelow are the available Time Slots for Vishakha:\n\n' + '\n'.join(available_slots) + '\n'
                    }
                }
            ]
            # Sending the batch update request to the Google Docs API
            service_docs.documents().batchUpdate(documentId=documentId, body={'requests': requests}).execute()

            print("Available time slots have been written to the Google Doc.")
        else:
            print("No available time slots to write to the Google Doc.")

    except HttpError as e:
        print(e)



def create_event(start_eventTime,end_eventTime):
    # Create an event
    print("*****ST",start_eventTime)
    print("*****ET",end_eventTime)
    event = {
        'summary': 'Test Event',
        'start': {
            'dateTime': start_eventTime,  # Start time in ISO format
            'timeZone': 'UTC',  # Timezone
            },
        'end': {
            'dateTime': end_eventTime,  # End time in ISO format
            'timeZone': 'UTC',  # Timezone
        },
    }
    print("\nStart time:::::",start_eventTime)
    print("End time:::::",end_eventTime)

    print("\nIn create_event function!!!",event)
    return event

def booking_details_retrieval(query):
    retrieve_sentence = 'Book calendar event for'
    # retrieve_sentence = 'Could you please book the time slot for'
    
    if retrieve_sentence in query:
        print('Sure will book the calendar event as requested')
        time_slot_info = query.split(retrieve_sentence)[1].strip()
        # time_slot_info = query.split(retrieve_sentence)
        print("The time slot info is:::::::",time_slot_info )
        print("\n Got booking slot information successfully!!!!!")

        # Splitting the time_slot_info to retrieve start and end time to pass it to the event calender
        Day,start_eventTime,_,end_eventTime = time_slot_info.split()
        print(Day)
        print(start_eventTime)
        print(end_eventTime)
        event = create_event(start_eventTime,end_eventTime)
        insert_calender_event(event)



def insert_calender_event(event):
    print("\nInside insert_calender_event!!!! ")
    print(event)

    creds = handling_credentials(SCOPES)

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = dt.datetime.now().isoformat() + 'Z'
        # event = event
        print("In insert calender event display:::",event)

        # Insert the event
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created:', created_event['id'])

        AutomaticEventRetrievalToDoc()
        googledoc_content_retrival()

          
    except HttpError as e:
        print(e)

def googledoc_content_retrival():

    creds = handling_credentials(SCOPES)
   
    try:
        service = build('docs', 'v1', credentials=creds)
        document = service.documents().get(documentId=documentId).execute()

        print(f"\nThe title of the document is: {document.get('title')}\n")

        # Get the content of the document
        content = document.get('body', {}).get('content', [])
        # document_body = document.get('body')
        # print("Document body is:",document_body)
        # print("\nContent of the file is",content)

        # Iterate through the content and print it
        text =''
        for element in content:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                # print('\nParagraph retrieval:::', paragraph)
                elements = paragraph.get('elements', [])
                # print('\nElements Retrieval',elements)
                for elem in elements:
                    # print('Elem is',elem)
                    if 'textRun' in elem:
                        # print('\nTextRun_content',elem['textRun']['content'])
                        text += elem['textRun']['content']
        # print(text)
        
        # Saving the content of the retrieved google doc
        output_path = os.path.join(output_folder, output_file)
        with open(output_path,'w', encoding='utf-8') as f:
            f.write(text)
        
        print("Google doc content saved successfully to:::",output_path)

    except HttpError as e:
        print(e)
    



def chatgpt_integration():
    while True:
        query = input("Enter your prompt: ")
        
        #For loadinding individual text file
        # loader = TextLoader('data_final.txt')

        #For loading complete directory
        loader = DirectoryLoader(output_folder,glob="*.txt")
        index = VectorstoreIndexCreator().from_loaders([loader])
        # print(index.query(query))
        # print(3)
        
        print(index.query(query, llm = ChatOpenAI()))
        booking_details_retrieval(query)
       

if __name__ == '__main__':
    AutomaticEventRetrievalToDoc()
    googledoc_content_retrival()
    chatgpt_integration()

