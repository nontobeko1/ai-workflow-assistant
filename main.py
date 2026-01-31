import os
import re
from datetime import datetime
from dotenv import load_dotenv

import gspread
from google.oauth2.service_account import Credentials
from transformers import pipeline


# -----------------------------
# Config / Environment
# -----------------------------
load_dotenv(dotenv_path=".env", override=True)

GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "AI_Adventurer_Logs")
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDS_JSON", "service_account.json")


# -----------------------------
# Helpers: Input
# -----------------------------
def get_email_input() -> str:
    print("\nPaste the support email below. Press Enter on a blank line to finish:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    email_text = "\n".join(lines).strip()
    if not email_text:
        raise ValueError("No email content provided.")
    return email_text


# -----------------------------
# Helpers: Extraction (Name/Topic/Urgency)
# -----------------------------
def extract_customer_name(email_text: str):
    match = re.search(r"\bmy name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", email_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    lines = [l.strip() for l in email_text.splitlines() if l.strip()]
    if len(lines) >= 2:
        last = lines[-1]
        if re.match(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?$", last):
            return last

    return None


def classify_topic(email_text: str) -> str:
    text = email_text.lower()
    topic_keywords = {
        "Billing/Payments": ["payment", "paid", "invoice", "billing", "checkout", "charge", "refund", "card"],
        "Login/Account": ["login", "log in", "password", "account", "signin", "sign in", "locked", "reset"],
        "Bug/Error": ["bug", "error", "issue", "crash", "broken", "not working", "fails", "failure"],
        "Delivery/Orders": ["delivery", "shipping", "order", "tracking", "dispatch"],
        "Feature Request": ["feature", "request", "add", "would like", "enhancement"],
    }

    for topic, kws in topic_keywords.items():
        if any(k in text for k in kws):
            return topic
    return "General Support"


def classify_urgency(email_text: str) -> str:
    text = email_text.lower()
    high = ["urgent", "asap", "immediately", "critical", "down", "outage", "cannot", "unable", "losing sales"]
    medium = ["soon", "important", "priority", "affecting", "problem"]
    low = ["when you can", "no rush", "whenever", "minor", "just a question"]

    if any(k in text for k in high):
        return "High"
    if any(k in text for k in medium):
        return "Medium"
    if any(k in text for k in low):
        return "Low"
    return "Medium"


# -----------------------------
# AI: Summarisation (robust)
# -----------------------------
def summarize_email(email_text: str) -> str:
    """
    Robust summarization:
    - Tries the normal 'summarization' pipeline
    - If unavailable (older transformers), falls back to 'text2text-generation'
    """
    clipped = email_text.strip()
    if len(clipped) > 2000:
        clipped = clipped[:2000]

    model_name = "sshleifer/distilbart-cnn-12-6"

    # Try standard summarization pipeline first
    try:
        summarizer = pipeline("summarization", model=model_name)
        out = summarizer(clipped, max_length=60, min_length=20, do_sample=False)[0]
        return out.get("summary_text", "").strip() or "Summary unavailable."
    except Exception:
        # Fallback: text2text-generation (works on older pipeline registries)
        generator = pipeline("text2text-generation", model=model_name)
        out = generator(clipped, max_length=60, do_sample=False)[0]
        # For text2text-generation, key is usually "generated_text"
        return out.get("generated_text", "").strip() or "Summary unavailable."


# -----------------------------
# Google Sheets Logging
# -----------------------------
def connect_sheet():
    if not os.path.exists(GOOGLE_CREDS_JSON):
        raise FileNotFoundError(
            f"Google credentials file not found: {GOOGLE_CREDS_JSON}\n"
            "Ensure 'service_account.json' is in the project folder and the sheet is shared with the service account email."
        )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(GOOGLE_CREDS_JSON, scopes=scopes)
    gc = gspread.authorize(creds)

    sh = gc.open(GOOGLE_SHEET_NAME)
    ws = sh.sheet1
    return ws


def ensure_header(ws):
    header = ["Timestamp", "Customer", "Topic", "Urgency", "Summary", "Raw Email"]
    first_row = ws.row_values(1)
    if first_row != header:
        if not first_row:
            ws.append_row(header)
        else:
            ws.insert_row(header, 1)


def log_to_sheet(ws, customer, topic, urgency, summary, email_text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, customer, topic, urgency, summary, email_text]
    ws.append_row(row, value_input_option="USER_ENTERED")


# -----------------------------
# Main
# -----------------------------
def main():
    print("=== Intelligent Workflow Assistant (Hugging Face + Google Sheets) ===")

    try:
        email_text = get_email_input()

        print("\n✅ Running AI summarisation locally (Hugging Face)...")
        summary = summarize_email(email_text)

        customer = extract_customer_name(email_text)
        topic = classify_topic(email_text)
        urgency = classify_urgency(email_text)

        print("\n✅ Extracted Results:")
        print(f"Customer: {customer}")
        print(f"Topic: {topic}")
        print(f"Urgency: {urgency}")
        print(f"Summary: {summary}")

        print("\n✅ Connecting to Google Sheets...")
        ws = connect_sheet()
        ensure_header(ws)

        print("✅ Logging record to Google Sheets...")
        log_to_sheet(ws, customer, topic, urgency, summary, email_text)

        print("\n🎉 Done! Logged to Google Sheets successfully.")

    except Exception as e:
        print("\n❌ Error:")
        print(str(e))
        print("\nTroubleshooting tips:")
        print("- Run: pip install -U transformers torch accelerate sentencepiece")
        print("- Ensure service_account.json exists and Sheet is shared with service account email.")
        print("- Ensure GOOGLE_SHEET_NAME matches the sheet name exactly.")


if __name__ == "__main__":
    main()
