# audio.py
import pyaudio
import wave
import pyttsx3
from faster_whisper import WhisperModel

# ----------------------------
# Record audio from microphone
# ----------------------------
def record_audio(filename="input.wav"):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels,
                    rate=rate, input=True,
                    frames_per_buffer=chunk)

    print("🤖 Assistant: Recording started. Press Ctrl+C to stop.")
    frames = []
    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print("\n🤖 Assistant: Recording stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    print(f"🤖 Assistant: Audio saved as {filename}")

# ----------------------------
# Text-to-speech
# ----------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

# ----------------------------
# Transcribe audio to text
# ----------------------------
def transcribe_audio(filename="input.wav"):
    model = WhisperModel("small")  # small/base for CPU
    segments, info = model.transcribe(filename, beam_size=5)
    text = " ".join([segment.text for segment in segments])
    return text
