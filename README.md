## Overview

The **Intelligent Scheduling Assistant** leverages **GPT-based natural language understanding** to parse user messages, extract scheduling details, and automatically create events in **Google Calendar** via API integration.  

It also functions as a **chatbot**, responding to user queries in natural language about scheduling, availability, and calendar events.  

This project integrates **OpenAI**, **Google Docs**, and **Google Calendar**, supporting both manual and automatic retrieval of available time slots.

---

## Features

### Chatbot Functionality
- Converses naturally with the user using GPT  
- Handles request-response interactions  
- Answers scheduling-related queries  
- Automatically creates events in Google Calendar when requested  

### Basic Operations
The assistant can query data from **text files** or **folders**, with or without OpenAI integration:

1. **Querying Own Data (Text File)**
   - Without OpenAI integration  
   - With OpenAI integration  

2. **Querying Own Data (Folder)**
   - Without OpenAI integration  
   - With OpenAI integration  

These operations can also be applied to content retrieved from **Google Docs**.

### Advanced Integration
1. **Manual Time Slots**
   - Full integration with ChatGPT, Google Docs, and Google Calendar  
   - Available time slots are manually added to Google Docs  

2. **Automatic Time Slots**
   - Automatic retrieval of available time slots from Google Calendar into Google Docs  
   - Creates events automatically based on extracted information  

---

## Technology Stack

- **Programming Language:** Python  
- **APIs & Services:**  
  - OpenAI GPT API  
  - Google Calendar API  
  - Google Docs API  
- **Data Handling:** Text files, folders, Google Docs  

---

## Usage

1. **Setup APIs**: Configure OpenAI and Google API credentials.  
2. **Prepare Data**: Store your schedule data in text files, folders, or Google Docs.  
3. **Run Queries**:  
   - Perform basic operations with or without OpenAI integration  
   - Retrieve content from Google Docs if needed  
4. **Interact with Chatbot**:  
   - Ask questions about scheduling  
   - Request event creation  
5. **Schedule Events**:  
   - For manual time slots: input availability in Google Docs  
   - For automatic time slots: retrieve availability from Google Calendar  
6. **Automatic Event Creation**: The assistant parses messages and creates events in Google Calendar automatically.

---

## Highlights

- Fully automates scheduling workflow  
- Functions as a natural-language chatbot  
- Supports multiple modes of querying and integration  
- Combines GPT understanding with Google Workspace APIs  
