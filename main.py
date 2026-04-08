"""
main.py — Entry Point for the Dustin Henderson Voice Agent

This is the main loop that ties everything together:
1. Initializes the ADK session
2. Listens for voice input (speech-to-text)
3. Sends input to the ADK agent
4. Speaks the response (text-to-speech)
5. Repeats until the user says "quit" or "exit"

=== HOW ADK CONCEPTS FLOW THROUGH THIS APP ===

  [Voice Input] → (speech-to-text)
       ↓
  [main.py] → calls get_agent_response(text)
       ↓
  [agent.py] → Runner sends text to Agent (SESSION)
       ↓
  [Agent/LLM] → Decides: respond directly OR call a TOOL
       ↓
  [tools.py] → Tool executes, updates STATE via ToolContext
       ↓
  [Agent/LLM] → Crafts final response using tool output + personality
       ↓
  [agent.py] → Saves to MEMORY, returns response text
       ↓
  [Voice Output] → (text-to-speech)
       ↓
  [Loop continues...]

Run: python main.py
"""

import asyncio
import os

from dotenv import load_dotenv

# Load environment variables from .env file
# This is where your GOOGLE_API_KEY lives
load_dotenv()

# Verify API key is set
if not os.getenv("GOOGLE_API_KEY"):
    print("=" * 60)
    print("❌  ERROR: GOOGLE_API_KEY not found!")
    print()
    print("To fix this:")
    print("  1. Get a free API key from https://aistudio.google.com/")
    print("  2. Create a .env file in this directory")
    print("  3. Add: GOOGLE_API_KEY=your_key_here")
    print("=" * 60)
    exit(1)

from agent import get_agent_response, _create_session
from voice_input import listen
from voice_output import speak


# ============================================================
# BANNER
# ============================================================

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🧇  DUSTIN HENDERSON — AI Voice Assistant  🧇             ║
║                                                              ║
║    Powered by Google Agent Development Kit (ADK)             ║
║                                                              ║
║    "This is like Cerebro, but for your BRAIN!"               ║
║                                                              ║
║    Commands:                                                 ║
║      • Speak naturally to ask questions                      ║
║      • Say "quit" or "exit" to end                           ║
║      • Say "type" to switch to keyboard input                ║
║                                                              ║
║    ADK Concepts in action:                                   ║
║      🤖 Agent  │  🔧 Tools  │  📋 Session                    ║
║      📊 State  │  🧠 Memory                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


async def main():
    """Main application loop."""
    print(BANNER)

    # === ADK CONCEPT: SESSION INITIALIZATION ===
    # Create the session BEFORE the conversation loop starts.
    # This sets up the state dictionary and prepares the agent.
    print("🔄  Initializing Dustin's brain (ADK session)...")
    await _create_session()
    print("✅  Session ready! Dustin is online.\n")

    # Greeting
    greeting = (
        "Hey! It's Dustin Henderson here, ready to explain stuff! "
        "Think of me as your personal Cerebro for tech knowledge. "
        "What do you wanna know? Just talk to me!"
    )
    speak(greeting)

    # Track input mode — voice by default, can switch to typing
    use_voice = True

    # === MAIN CONVERSATION LOOP ===
    while True:
        try:
            # Step 1: Get user input (voice or keyboard)
            if use_voice:
                user_input = listen()
                if not user_input:
                    # No speech detected — prompt to try again
                    print("💡  [Tip: Speak clearly, or say 'type' to use keyboard]")
                    continue
            else:
                user_input = input("\n⌨️   You: ").strip()
                if not user_input:
                    continue

            # Step 2: Check for control commands
            lower_input = user_input.lower().strip()

            if lower_input in ("quit", "exit", "bye", "goodbye"):
                farewell = (
                    "Alright, catch you later! Remember — "
                    "friends don't lie, and neither does good code! "
                    "Over and out!"
                )
                speak(farewell)
                break

            if lower_input == "type":
                use_voice = not use_voice
                mode = "keyboard" if not use_voice else "voice"
                print(f"🔄  Switched to {mode} input mode!")
                continue

            # Step 3: Send to the ADK agent and get response
            # This is where ALL the ADK magic happens:
            # Agent → Tools → State → Memory → Response
            print("\n🧠  [Dustin is thinking...]")
            response = await get_agent_response(user_input)

            # Step 4: Speak the response
            speak(response)

        except KeyboardInterrupt:
            print("\n\n👋  [Ctrl+C detected — Dustin signing off!]")
            break
        except Exception as e:
            print(f"\n💥  [Something went wrong: {e}]")
            print("     [Like a Demogorgon attack — but we'll recover!]\n")
            continue

    print("\n🔌  [Session ended. See you in Hawkins!]\n")


if __name__ == "__main__":
    asyncio.run(main())
