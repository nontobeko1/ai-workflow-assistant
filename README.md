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
