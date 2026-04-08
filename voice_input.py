"""
voice_input.py — Speech-to-Text Module

Captures audio from the microphone and converts it to text.
Uses the SpeechRecognition library with Google's free speech API.

Think of this like Dustin's radio receiver — it listens for signals
and translates them into something the party can understand!
"""

import speech_recognition as sr


def listen() -> str:
    """
    Listen to the microphone and return the recognized text.
    
    Returns:
        The recognized speech as a string, or an empty string on failure.
    """
    recognizer = sr.Recognizer()

    # Adjust for ambient noise sensitivity
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("\n🎙️  [Dustin is listening... speak now!]")

        # Brief ambient noise adjustment
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            # Listen with a timeout so it doesn't hang forever
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            print("🔄  [Processing your signal...]")

            # Use Google's free speech recognition API
            text = recognizer.recognize_google(audio)
            print(f"📡  You said: \"{text}\"")
            return text

        except sr.WaitTimeoutError:
            print("⏰  [No signal detected — try again!]")
            return ""
        except sr.UnknownValueError:
            print("❓  [Couldn't decode that signal — too much static!]")
            return ""
        except sr.RequestError as e:
            print(f"🚫  [Radio tower is down! Speech API error: {e}]")
            return ""
