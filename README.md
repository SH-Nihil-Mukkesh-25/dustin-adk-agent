# Dustin ADK Agent

## Overview

The Dustin ADK Agent is a voice-capable AI assistant built using the Google Agent Development Kit (ADK). This project demonstrates the usage of the ADK for building robust LLM-driven applications with speech recognition and text-to-speech capabilities. The assistant embodies a specific personality prompt and is designed to explain technical concepts using targeted analogies.

## Architecture and Core ADK Concepts

This project implements several fundamental concepts provided by the Google ADK:

- **Agent**: An instance configured with specialized instructions, utilizing the `gemini-2.5-flash` model.
- **Tools**: Custom functions registered with the agent, enabling it to execute operations like generating examples and formatting explanations.
- **Session**: State storage managed by the `InMemorySessionService`, allowing the agent to maintain context across conversation turns.
- **State**: A persistent dictionary containing context (e.g., questions asked and recent topics) that is accessible and mutable by tools during runtime.
- **Runner**: The orchestrator which bridges the user input, the session state, and the core agent.

## Project Structure

- `main.py` - Core execution loop, handling session initialization, voice inputs, and standard output.
- `agent.py` - Configuration of the LLM model, system instructions, session instantiation, and Runner creation.
- `tools.py` - Definitions for external tools executed by the agent.
- `memory.py` - Custom context and history tracking separated from the default ADK session logs.
- `voice_input.py` - Speech-to-text integration using PyAudio and SpeechRecognition.
- `voice_output.py` - Text-to-speech implementation utilizing pyttsx3.

## Setup and Installation

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   Copy `.env.example` to `.env` and register your API key:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

Execute the main script to start the agent:

```bash
python main.py
```

Command options:
- Speak naturally to interact
- Say "type" to format inputs via keyboard
- Say "quit" or "exit", or press Ctrl+C to terminate the session
