"""
voice_output.py — Text-to-Speech Module

Converts the agent's text response into spoken audio.
Uses pyttsx3 for OFFLINE text-to-speech (no API key needed).

This is like Dustin's radio transmitter — once he figures out the answer,
he broadcasts it back to the party!
"""

import pyttsx3

def speak(text: str) -> None:
    """
    Convert text to speech and play it through the speakers.
    
    Args:
        text: The text to speak aloud.
    """
    if not text:
        return

    print(f"\n🔊  [Dustin says]: {text}\n")

    try:
        # Initialize locally per call to prevent asyncio/event-loop conflicts
        # which often cause pyttsx3 to silently fail after the first run.
        engine = pyttsx3.init()
        engine.setProperty("rate", 185)      # Slightly faster — Dustin talks fast!
        engine.setProperty("volume", 1.0)    # Full volume
        
        engine.say(text)
        engine.runAndWait()
        
        # Stop the engine to free up the win32com instance safely
        engine.stop()
    except Exception as e:
        # Fallback: if TTS fails, the text is already printed above
        print(f"⚠️  [Voice output error: {e} — but you can read it above!]")
