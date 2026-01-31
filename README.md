# Intelligent Workflow Assistant
AI Adventurer Quest

## Overview
This project is a lightweight AI-powered assistant designed to help a small customer
support team automate the handling of incoming support emails.

The system analyses a support email, extracts key information, determines urgency,
summarises the issue using AI, and automatically logs the result into Google Sheets.

This solution demonstrates the practical use of AI, automation, and API integration
in a real-world workflow.

---

## Features
- Accepts email-style text input
- AI-driven email summarisation using a Hugging Face transformer model
- Automatic extraction of:
  - Customer name
  - Topic
  - Urgency level
- Automated logging to Google Sheets using Google APIs
- End-to-end execution from input to task tracking

---

## Tools & Technologies
- Python 3.12
- Hugging Face Transformers (local AI model)
- Google Sheets API
- Google Drive API
- gspread (Python Google Sheets client)
- dotenv for configuration management

---

## How It Works
1. A support email is entered via the command line
2. The email is summarised using a local AI model
3. Key details such as customer, topic, and urgency are extracted
4. The structured output is automatically written to a Google Sheet

---

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

---

## Demo Evidence

This repository includes visual evidence demonstrating the full end-to-end
execution of the Intelligent Workflow Assistant.

The demo screenshots show:

- Command-line execution of the application
- AI-generated extraction of customer name, topic, urgency, and summary
- Successful automated logging of results into Google Sheets using Google APIs

These screenshots confirm that the solution works as intended, from email input
through AI processing to automated task tracking.

🔮 Easy Extensibility & Next-Step Ideas
This solution was intentionally designed to be lightweight and modular, making it easy to extend in future iterations. Possible next steps include:

1️⃣ Email Inbox Integration
Instead of manual email input, the assistant could be connected directly to an email inbox (e.g. Gmail or Outlook) using their APIs. Incoming support emails would be processed automatically in real time without user intervention.

2️⃣ Workflow Automation with n8n
The Python script could be wrapped inside an n8n workflow to:

Trigger on new emails

Route high-urgency tickets to notifications (Slack, Teams)

Create structured tasks in tools such as Trello, Notion, or Jira

This would turn the assistant into a fully no-code/low-code automation pipeline.

3️⃣ Web-Based User Interface
A simple web UI (Flask or FastAPI) could allow non-technical users to submit emails through a browser instead of the command line. This would make the tool usable by actual support teams.

4️⃣ Sentiment & SLA Analysis
Additional AI models could be added to:

Detect customer sentiment (frustrated, neutral, satisfied)

Automatically assign response SLAs based on urgency and sentiment

Track resolution times using the existing Google Sheets log

5️⃣ Multi-Channel Support Expansion
The assistant could be extended to handle messages from other platforms such as:

Live chat

Contact forms

WhatsApp or social media support channels

All inputs could be normalised into the same automated workflow.

6️⃣ Analytics & Reporting Dashboard
The structured data already collected in Google Sheets could be visualised using tools like:

Google Data Studio / Looker

Power BI

This would enable managers to analyse support trends, volume, and response priorities over time.


