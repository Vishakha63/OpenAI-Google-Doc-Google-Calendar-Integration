import os

import sys
import warnings
import constants

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.llms import openai
from langchain_community.chat_models import ChatOpenAI

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = constants.APIKEY

SCOPES =["https://www.googleapis.com/auth/documents"]

documentId='1FGomq-T7vbI_3tDMAGQYWLqpJhX71aQAX4Qi2hQzHFE'

#Locating the path of the main python file which is run

main_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

output_folder = os.path.join(main_folder,'demo_chat_googledoc_simple')
output_file = 'datagoogledoc.txt'
output_file1 = 'FromGoogleDoc_data_textDir.txt'

def googledoc_content_retrival():
    credentials = None
    if os.path.exists("token1.json"):
        credentials = Credentials.from_authorized_user_file("token1.json",SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_latest.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token1.json',"w") as token:
            token.write(credentials.to_json())
    try:
        service = build('docs', 'v1', credentials=credentials)
        document = service.documents().get(documentId=documentId).execute()

        print(f"\nThe title of the document is: {document.get('title')}\n")

        # Get the content of the document
        content = document.get('body', {}).get('content', [])
        # content = document.get('body')
        # print("Content of the file is",content)

        # Iterate through the content and print it
        text =''
        for element in content:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                elements = paragraph.get('elements', [])
                for elem in elements:
                    if 'textRun' in elem:
                        text += elem['textRun']['content']
        # print(text)
        
        # with open(output_file1,'w', encoding='utf-8') as f:
        #     f.write(text)
        # Saving the content of the retrieved google doc
        output_path = os.path.join(output_folder, output_file)
        with open(output_path,'w', encoding='utf-8') as f:
            f.write(text)
        
        print("Google doc content saved successfully to:::",output_path)
        # print("Google doc content saved successfully to:::",output_file1)

    except HttpError as e:
        print(e)


def chatgpt_integration():

    while True:
        query = input("Enter your prompt: ")

        #For loadinding individual text file
        # loader = TextLoader('FromGoogleDoc_data_textDir.txt')

        #For loading complete directory
        loader = DirectoryLoader(output_folder,glob="*.txt")
        index = VectorstoreIndexCreator().from_loaders([loader])

        print(index.query(query))
        # print(index.query(query, llm = ChatOpenAI()))
    

if __name__ == '__main__':
    googledoc_content_retrival()
    chatgpt_integration()



