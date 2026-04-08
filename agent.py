"""
agent.py — ADK Agent Configuration & Response Handler

=== ADK CONCEPTS DEMONSTRATED HERE ===
1. AGENT   — Creating an Agent instance with personality, model, and tools
2. TOOLS   — Registering tool functions with the agent
3. SESSION — Creating and managing sessions via InMemorySessionService
4. STATE   — Initializing and tracking state within the session
5. RUNNER  — Using the Runner to orchestrate agent execution

This is the BRAIN of the application — where Dustin comes to life!
"""

import asyncio

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from tools import explain_concept_tool, example_generator_tool
from memory import ConversationMemory


# ============================================================
# DUSTIN HENDERSON — PERSONALITY PROMPT (MANDATORY)
# ============================================================
# This is the system instruction that shapes the agent's personality.
# The LLM will follow these rules for EVERY response.

DUSTIN_PROMPT = """You are Dustin Henderson from Stranger Things.

Personality:
- Nerdy, funny, energetic
- You LOVE science and explaining things
- You speak like a best friend who just discovered something amazing

Communication Rules:
- ALWAYS explain using Stranger Things references
- Use analogies like:
  - The Upside Down (for hidden/parallel systems, recursion, alternate states)
  - Demogorgon (for bugs, errors, threats, complex problems)
  - Hawkins Lab (for behind-the-scenes processes, compilers, servers)
  - D&D campaigns (for strategies, algorithms, planning)
  - Radios and signals (for networking, APIs, communication)
  - Cerebro (for amplifying, scaling, boosting performance)
  - The Mind Flayer (for distributed systems, controllers, orchestrators)
  - Eleven's powers (for powerful features, abstractions, magic methods)

Examples of how you talk:
- "Think of recursion like opening a gate to the Upside Down again and again — each time you go deeper, you're in another layer, and you gotta find your way back!"
- "This is like how I built Cerebro to amplify radio signals — APIs work the same way, they amplify what your app can do!"
- "A Demogorgon just crashed your code? That's a runtime error, dude. We gotta debug this like we're tracking it through the tunnels."

SCIENCE MODE:
- Trigger when user asks "how" or "explain" or any technical question
- Break the explanation into clear steps
- STILL use Stranger Things references in every step
- Number the steps like levels in a D&D campaign

STRICT RULES:
- NEVER give plain textbook answers
- EVERY response MUST include at least one Stranger Things analogy
- Keep responses conversational and fun — you're talking to a friend
- If the user asks something non-technical, still stay in character as Dustin
- Use exclamation marks! You're excited about EVERYTHING!
- Occasionally reference "the party" (your friend group)

MEMORY CONTEXT (what you remember from this conversation):
{memory_summary}

CURRENT STATE:
- Questions asked so far: {number_of_questions}
- Last topic discussed: {last_topic}
"""


# ============================================================
# ADK CONCEPT: AGENT
# ============================================================
# The Agent class is the core building block of ADK.
# It wraps an LLM with instructions, tools, and configuration.
# The agent uses the model to reason about user input and decide
# when to call tools vs. respond directly.

dustin_agent = Agent(
    name="dustin_henderson",                    # Unique agent identifier
    model="gemini-2.5-flash",                   # The LLM model to use
    description=(
        "A voice assistant inspired by Dustin Henderson from Stranger Things. "
        "Explains coding and tech concepts using Stranger Things analogies."
    ),
    instruction=DUSTIN_PROMPT,                  # System prompt (personality)
    tools=[                                     # === ADK CONCEPT: TOOLS ===
        explain_concept_tool,                   # Tool 1: Explain concepts
        example_generator_tool,                 # Tool 2: Generate examples
    ],
    # Tools are registered here — the agent reads each tool's docstring
    # to understand WHEN and HOW to use them. The LLM decides autonomously.
)


# ============================================================
# ADK CONCEPT: SESSION SERVICE
# ============================================================
# The SessionService manages conversation sessions. Each session has:
# - A unique ID
# - Conversation history (messages back and forth)
# - A state dictionary (key-value pairs that persist across turns)
#
# InMemorySessionService stores everything in RAM — perfect for learning.
# In production, you'd use DatabaseSessionService or VertexAISessionService.

session_service = InMemorySessionService()


# Constants for this app's session
APP_NAME = "dustin_agent_app"
USER_ID = "user_01"


# ============================================================
# ADK CONCEPT: RUNNER
# ============================================================
# The Runner orchestrates the agent execution loop:
# 1. Takes user input
# 2. Sends it to the agent (LLM)
# 3. If the agent calls a tool → executes the tool → sends result back
# 4. Repeats until the agent produces a final text response
# 5. Manages session history automatically
#
# Think of the Runner as the Dungeon Master — it manages the game flow!

runner = Runner(
    app_name=APP_NAME,
    agent=dustin_agent,
    session_service=session_service,
)


# ============================================================
# MEMORY INSTANCE
# ============================================================
# Our custom memory store (separate from ADK's built-in session history).
# This demonstrates how you'd build a memory layer for personalization.

memory = ConversationMemory()


# ============================================================
# SESSION + STATE INITIALIZATION
# ============================================================



# We'll store the session object here after async creation
_session = None


async def _create_session():
    """
    Create a new ADK session with initial state values.
    
    === ADK CONCEPT: SESSION CREATION ===
    Sessions are created via the session service. Each session gets:
    - app_name: Groups sessions by application
    - user_id: Identifies the user
    - state: Initial key-value pairs the agent can read/write
    
    === ADK CONCEPT: STATE ===
    State is a dictionary attached to the session. Tools can read/write it
    via ToolContext. The agent can also reference state values in its prompt
    using curly braces like {last_topic}.
    
    State keys used in this app:
    - last_topic: The most recent topic the user asked about
    - number_of_questions: How many questions the user has asked
    - topics_discussed: List of all topics covered
    - memory_summary: Text summary from our custom memory module
    """
    global _session

    # === ADK CONCEPT: STATE INITIALIZATION ===
    # These initial values are available to the agent from the first turn.
    # Tools update these values as the conversation progresses.
    initial_state = {
        "last_topic": "nothing yet",
        "number_of_questions": 0,
        "topics_discussed": [],
        "memory_summary": "No previous conversation — this is a fresh start!",
    }

    _session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    print(f"📋  [Session created: {_session.id}]")
    return _session


async def get_agent_response(user_input: str) -> str:
    """
    Send user input to the Dustin agent and get a response.
    
    This function demonstrates the complete ADK flow:
    1. Ensure session exists (SESSION concept)
    2. Update memory context in state (STATE + MEMORY concepts)
    3. Run the agent via Runner (RUNNER concept)
    4. Agent may call tools (TOOLS concept)
    5. Collect the final response
    6. Store in memory (MEMORY concept)
    
    Args:
        user_input: The text from the user (from speech-to-text).
        
    Returns:
        The agent's text response (to be sent to text-to-speech).
    """
    global _session

    # Step 1: Ensure we have a session
    if _session is None:
        await _create_session()

    # Step 2: Update the memory summary in session state
    # This injects our custom memory context into the agent's prompt
    # via the {memory_summary} template variable in DUSTIN_PROMPT.
    _session.state["memory_summary"] = memory.get_summary()

    # Step 3: Create the user message in ADK's expected format
    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)],
    )

    # Step 4: Run the agent and collect the response
    # runner.run_async() yields events as the agent processes.
    # Events include tool calls, intermediate reasoning, and final text.
    response_text = ""
    async for event in runner.run_async(
        session_id=_session.id,
        user_id=USER_ID,
        new_message=user_message,
    ):
        # Collect text parts from the agent's response
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text

    # Step 5: Store this turn in our custom memory
    if response_text:
        memory.add_turn(user_input, response_text)
        # Track topics from state (tools update this)
        for topic in _session.state.get("topics_discussed", []):
            memory.add_topic(topic)

    return response_text or "Whoa, my brain glitched — like the Upside Down flickered! Ask me again?"
