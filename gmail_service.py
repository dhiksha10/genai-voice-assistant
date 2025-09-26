# gmail_service.py
from email.mime.text import MIMEText
import base64

def send_email(service, recipient, subject, body, speak_callback=None):
    """
    Send an email using Gmail API.
    
    Args:
        service: Authenticated Gmail service
        recipient: str
        subject: str
        body: str
        speak_callback: optional, function to speak success message
    """
    try:
        message = MIMEText(body)
        message["to"] = recipient
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {"raw": raw}
        service.users().messages().send(userId="me", body=message_body).execute()
        msg = f"📧 Email sent to {recipient}"
        print(msg)
        if speak_callback:
            speak_callback(msg)
    except Exception as e:
        print("❌ Failed to send email:", e)
        if speak_callback:
            speak_callback("Failed to send email.")
