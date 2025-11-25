import os
import sys
import warnings
import constants

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
documentId='1FGomq-T7vbI_3tDMAGQYWLqpJhX71aQAX4Qi2hQzHFE'

main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

output_folder = os.path.join(main_folder,'demo_complete_doc_cal_openai')
output_file = 'datagoogledoc1.txt'

warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = constants.APIKEY

def handling_credentials(SCOPES):
    credentials = None
    if os.path.exists("token2.json"):
        credentials = Credentials.from_authorized_user_file("token2.json",SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_latest.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token2.json',"w") as token:
            token.write(credentials.to_json())
    print(credentials)
    return credentials


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
    retrieve_sentence = 'Scheduling an event for'
    if retrieve_sentence in query:
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


def remove_time_slot_from_doc(start_eventTime, end_eventTime):
    # Cleaning up and formatting the start and end times
    formatted_time_slot = f"{start_eventTime} to {end_eventTime}"

    creds = handling_credentials(SCOPES)
   
    try:
        service = build('docs', 'v1', credentials=creds)
        document = service.documents().get(documentId=documentId).execute()

        '''
        content = document.get('body', {}).get('content', [])
        updated_content = []

        # Iterating through the content and filtering out the booked time slot to remove the slot from the Google document
        for element in content:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                elements = paragraph.get('elements', [])

                # Flag to determine if the paragraph contains the booked time slot
                contains_time_slot = False

                for elem in elements:
                    if 'textRun' in elem and 'content' in elem['textRun']:
                        text_content = elem['textRun']['content']
                        if formatted_time_slot in text_content:
                            contains_time_slot = True
                            break

                # Adding the paragraph to the updated content if it doesn't contain the booked time slot
                if not contains_time_slot:
                    updated_content.append(element)
                    

        # Updating the document with the modified content
        
        document['body']['content'] = updated_content
        '''

        
        
        # Providing a non-empty substring match text
        substring_match_text = formatted_time_slot
        service.documents().batchUpdate(documentId=documentId, body={'requests': [{'replaceAllText': {'containsText': {'text': substring_match_text}, 'replaceText': ''}}]}).execute()


        print("Time slot removed from the Google Doc.")

        # Reflecting the changes made in the google doc to the local data repository
        googledoc_content_retrival()

    except HttpError as e:
        print(e)



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

        # Remove the booked time slot from the Google Doc
        start_eventTime = event['start']['dateTime']
        end_eventTime = event['end']['dateTime']
        remove_time_slot_from_doc(start_eventTime, end_eventTime)



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

        print(index.query(query))
        # print(index.query(query, llm = ChatOpenAI()))
        booking_details_retrieval(query)

if __name__ == '__main__':
    googledoc_content_retrival()
    chatgpt_integration()

