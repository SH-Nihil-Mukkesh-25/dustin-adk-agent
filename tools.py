"""
tools.py — Custom Tools for the Dustin Henderson Agent

=== ADK CONCEPT: TOOLS ===
Tools are Python functions that extend an agent's capabilities beyond
what the LLM can do on its own. The agent (LLM) decides WHEN to call
a tool based on the user's input and the tool's description.

Key rules for ADK tools:
1. Each tool is a plain Python function
2. The function's docstring becomes the tool description (the LLM reads this!)
3. Type hints on parameters tell the LLM what arguments to provide
4. Adding `tool_context: ToolContext` gives access to session state
5. Tools are registered with the Agent via the `tools=[]` parameter

Think of tools like Dustin's gadgets — Cerebro, the compass, his radio.
The agent picks the right gadget for the job!
"""

from google.adk.tools import ToolContext


# ============================================================
# TOOL 1: explain_concept_tool
# ============================================================
# This tool is called when the user asks the agent to explain something.
# The agent decides to use this tool based on its docstring description.

def explain_concept_tool(concept: str, tool_context: ToolContext) -> dict:
    """
    Explains a technical concept in a simplified way.
    Use this tool when the user asks you to explain, describe, or break down
    a concept — especially coding, science, or tech topics.
    Returns a structured explanation with key points.

    Args:
        concept: The concept or topic the user wants explained.
    """

    # === ADK CONCEPT: STATE (accessed via ToolContext) ===
    # ToolContext gives us access to the session's state dictionary.
    # We use this to track what the user has been asking about.
    # State persists across turns within the same session.

    state = tool_context.state

    # Update state: track the last topic discussed
    state["last_topic"] = concept

    # Update state: increment the question counter
    question_count = state.get("number_of_questions", 0) + 1
    state["number_of_questions"] = question_count

    # Track all topics in state for memory/context
    topics_list = state.get("topics_discussed", [])
    if concept not in topics_list:
        topics_list.append(concept)
    state["topics_discussed"] = topics_list

    # Return structured data — the LLM will use this to craft its response
    # with the Dustin Henderson personality from the system prompt
    return {
        "concept": concept,
        "explanation_hint": (
            f"Break down '{concept}' into 3 simple steps. "
            f"Use Stranger Things analogies for each step. "
            f"This is question #{question_count} from the user."
        ),
        "question_number": question_count,
        "status": "ready_to_explain",
    }


# ============================================================
# TOOL 2: example_generator_tool
# ============================================================
# This tool generates practical examples for a given topic.
# The agent uses this when the user wants concrete examples or use cases.

def example_generator_tool(topic: str, num_examples: int, tool_context: ToolContext) -> dict:
    """
    Generates practical examples and analogies for a given topic.
    Use this tool when the user asks for examples, use cases, analogies,
    or wants to see how something works in practice.

    Args:
        topic: The topic to generate examples for.
        num_examples: How many examples to generate (1-5).
    """

    # === ADK CONCEPT: STATE (reading + writing) ===
    # We can both read existing state and write new values.
    # This demonstrates state continuity across tool calls.

    state = tool_context.state

    # Clamp number of examples to a reasonable range
    num_examples = max(1, min(num_examples, 5))

    # Update state tracking
    state["last_topic"] = topic
    question_count = state.get("number_of_questions", 0) + 1
    state["number_of_questions"] = question_count

    # Check if this topic was previously explained (state continuity!)
    topics_discussed = state.get("topics_discussed", [])
    previously_explained = topic in topics_discussed

    if topic not in topics_discussed:
        topics_discussed.append(topic)
        state["topics_discussed"] = topics_discussed

    # Return structured data for the LLM to work with
    return {
        "topic": topic,
        "num_examples_requested": num_examples,
        "previously_explained": previously_explained,
        "example_hint": (
            f"Generate {num_examples} practical example(s) for '{topic}'. "
            f"Each example MUST use a Stranger Things analogy. "
            f"If previously explained, build on the earlier explanation."
        ),
        "question_number": question_count,
        "status": "ready_to_generate",
    }
