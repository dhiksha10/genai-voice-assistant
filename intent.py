import subprocess
import json
import sys

OLLAMA_PATH = r"C:\Users\Amit\AppData\Local\Programs\Ollama\Ollama.exe"

def extract_intent_llama(text_command):
    prompt = (
        "You are a strict JSON parser assistant. "
        "Do NOT include any explanations. "
        "Extract the intent and entities from this command: "
        f"\"{text_command}\". "
        "Return only valid JSON with these keys: "
        "- intent: 'email' or 'meeting', "
        "- recipient, subject, body (for email), "
        "- title, date, time, attendees (for meetings). "
        "Example output:\n"
        "{\n"
        '  "intent": "email",\n'
        '  "recipient": "example@gmail.com",\n'
        '  "subject": "Meeting Update",\n'
        '  "body": "The meeting is postponed."\n'
        "}"
    )

    try:
        # Use UTF-8 decoding and longer timeout
        result = subprocess.run(
            [OLLAMA_PATH, "run", "llama3", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",   # fix UnicodeDecodeError
            timeout=60          # increase timeout
        )
        print("Raw output:", result.stdout.strip())

        return json.loads(result.stdout.strip())
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out! Try simplifying the command or increasing timeout.")
        return {"intent": "unknown"}
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON from Ollama output")
        print("Raw:", result.stdout.strip())
        return {"intent": "unknown"}
    except Exception as e:
        print(f"❌ Ollama failed with exception: {e}")
        return {"intent": "unknown"}
