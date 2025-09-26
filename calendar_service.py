# calendar_service.py
def create_event(service, title, date, time, attendees, speak_callback=None):
    """
    Create a calendar event using Google Calendar API.
    
    Args:
        service: Authenticated Calendar service
        title: str
        date: str in 'YYYY-MM-DD'
        time: str in 'HH:MM' 24-hour format
        attendees: str, comma-separated emails
        speak_callback: optional, function to speak success message
    """
    try:
        event = {
            "summary": title,
            "start": {
                "dateTime": f"{date}T{time}:00",
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": f"{date}T{time}:00",
                "timeZone": "Asia/Kolkata"
            },
            "attendees": [{"email": a.strip()} for a in attendees.split(",")]
        }
        service.events().insert(calendarId="primary", body=event).execute()
        msg = f"📅 Event created: {title} on {date} at {time}"
        print(msg)
        if speak_callback:
            speak_callback(msg)
    except Exception as e:
        print("❌ Failed to create event:", e)
        if speak_callback:
            speak_callback("Failed to create calendar event.")

