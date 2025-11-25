Overview

This project implements an Intelligent Scheduling Assistant that leverages GPT-based natural language understanding to parse user messages, extract scheduling details, and automatically create events in Google Calendar via API integration.

In addition to scheduling automation, it also functions as a chatbot, responding to user queries and providing natural-language interactions regarding scheduling and availability.

The assistant integrates multiple services, enabling seamless interaction between OpenAI, Google Docs, and Google Calendar, with both manual and automatic retrieval of available time slots.

Features
Chatbot Functionality

Converses with the user naturally using GPT

Handles request-response messages

Answers questions about scheduling, availability, and calendar events

Automatically schedules events when requested

Basic Operations

The assistant can query data from text files or folders, with or without OpenAI integration:

Querying Own Data (Text File)

Without OpenAI integration

With OpenAI integration

Querying Own Data (Folder)

Without OpenAI integration

With OpenAI integration

These operations can also be applied to content retrieved from Google Docs.

Advanced Integration

Manual Time Slots

Complete integration of ChatGPT, Google Docs, and Google Calendar

Available time slots are manually added to Google Docs

Automatic Time Slots

Full integration with automatic retrieval of available time slots from Google Calendar into Google Docs

Scheduling events are automatically created based on the extracted information

Technology Stack

Programming Language: Python

APIs & Services:

OpenAI GPT API

Google Calendar API

Google Docs API

Data Handling: Text files, folders, Google Docs

Usage

Setup APIs: Configure OpenAI and Google API credentials.

Prepare Data: Store your schedule data in text files, folders, or Google Docs.

Run Queries:

Choose basic operations with or without OpenAI integration

Retrieve content from Google Docs if needed

Interact with Chatbot:

Ask questions about scheduling

Request event creation

Schedule Events:

For manual time slots: input available slots in Google Docs

For automatic time slots: retrieve availability from Google Calendar

Automatic Event Creation: The assistant parses user messages and creates events in Google Calendar automatically.

Highlights

Fully automates the scheduling workflow

Functions as a natural-language chatbot

Supports multiple modes of querying and integration

Combines GPT understanding with Google Workspace APIs
