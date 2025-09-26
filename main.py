# main.py
from audio import record_audio, speak, transcribe_audio
from intent import extract_intent_llama
from gmail_service import send_email
from calendar_service import create_event
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle, os

# Google API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.send", 
          "https://www.googleapis.com/auth/calendar.events"]

# ----------------------------
# Google API authentication
# ----------------------------
def get_google_services():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    gmail_service = build("gmail", "v1", credentials=creds)
    calendar_service = build("calendar", "v3", credentials=creds)
    return gmail_service, calendar_service

# ----------------------------
# Main flow
# ----------------------------
if __name__ == "__main__":
    # Authenticate Google APIs
    gmail_service, calendar_service = get_google_services()

    # Record audio
    record_audio("input.wav")
    text = transcribe_audio("input.wav")
    speak(f"You said: {text}")

    # Extract intent using LLaMA
    structured_data = extract_intent_llama(text)
    print("📌 Extracted:", structured_data)

    # If extraction failed, initialize empty structure
    if not structured_data.get("intent"):
        structured_data = {
            "intent": "",
            "recipient": "",
            "subject": "",
            "body": "",
            "title": "",
            "date": "",
            "time": "",
            "attendees": ""
        }

    # Allow user to edit fields
    confirm = input("Do you want to edit this? (y/n): ").lower()
    if confirm == "y":
        if structured_data["intent"] == "email" or structured_data["intent"] == "":
            structured_data["recipient"] = input(f"Recipient [{structured_data.get('recipient','')}]: ") or structured_data.get("recipient","")
            structured_data["subject"] = input(f"Subject [{structured_data.get('subject','')}]: ") or structured_data.get("subject","")
            structured_data["body"] = input(f"Body [{structured_data.get('body','')}]: ") or structured_data.get("body","")
            structured_data["intent"] = "email"
        elif structured_data["intent"] == "meeting" or structured_data["intent"] == "":
            structured_data["title"] = input(f"Title [{structured_data.get('title','')}]: ") or structured_data.get("title","")
            structured_data["date"] = input(f"Date (YYYY-MM-DD) [{structured_data.get('date','')}]: ") or structured_data.get("date","")
            structured_data["time"] = input(f"Time (HH:MM) [{structured_data.get('time','')}]: ") or structured_data.get("time","")
            structured_data["attendees"] = input(f"Attendees (comma-separated) [{structured_data.get('attendees','')}]: ") or structured_data.get("attendees","")
            structured_data["intent"] = "meeting"

    # Execute intent
    if structured_data["intent"] == "email":
        send_email(
            gmail_service,
            structured_data["recipient"],
            structured_data["subject"],
            structured_data["body"],
            speak  # speak callback
        )
        speak(f"✅ Email sent to {structured_data['recipient']} successfully!")
    elif structured_data["intent"] == "meeting":
        create_event(
            calendar_service,
            structured_data["title"],
            structured_data["date"],
            structured_data["time"],
            structured_data["attendees"],
            speak  # speak callback
        )
        speak(f"✅ Meeting '{structured_data['title']}' scheduled on {structured_data['date']} at {structured_data['time']}.")
    else:
        speak("⚠️ No valid intent detected.")
