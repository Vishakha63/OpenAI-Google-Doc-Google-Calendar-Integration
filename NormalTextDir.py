import os
import sys
import warnings
import constants

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.llms import openai
from langchain_community.chat_models import ChatOpenAI

warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = constants.APIKEY

while True:
    query = input("Enter your prompt: ")

    # Getting the path of the directory where the main python file is run from
    get_currentdir_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    # print(get_currentdir_path)

    # Getting the path of the text file
    path_textfile = os.path.join(get_currentdir_path,'data_textDir.txt')

    #For loadinding individual text file
    loader = TextLoader(path_textfile)

    #For loading complete directory
    #Getting the path of the Folder
    path_folder = os.path.join(get_currentdir_path,'demodir_chatgpt_main')
    # print(path_folder)

    # loader = DirectoryLoader(path_folder,glob="*.txt")
    index = VectorstoreIndexCreator().from_loaders([loader])

    print(index.query(query))

    # print(index.query(query, llm = ChatOpenAI()))
