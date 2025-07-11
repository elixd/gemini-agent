import os
from typing import Annotated, TypedDict
import datetime
import pytz

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain.tools import StructuredTool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

# Import existing project functions and scheduler
from functions import create_note, update_note, list_notes, read_note
from scheduler import Scheduler
from dashboard import build_dashboard_context

# --- Configuration ---
load_dotenv() # Load environment variables from .env file

# Ensure OPENROUTER_API_KEY is set
if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("OPENROUTER_API_KEY environment variable not set. Please set it in your .env file or environment.")

# Initialize the LLM with OpenRouter configuration
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0, # Set temperature to 0 for more deterministic behavior
)

# --- Define Tools ---
scheduler = Scheduler('schedule.json')

@tool
def get_current_time(location: str) -> str:
    """Get the current time in a specific location.

    Args:
        location (str): The name of the city or region (e.g., "New York", "London", "Tokyo").
    """
    try:
        # Attempt to get the timezone for the given location
        # This is a simplified approach; a more robust solution might use a timezone API
        timezone = pytz.timezone(location.replace(" ", "_").replace("-", "_").title())
        current_time = datetime.datetime.now(timezone)
        return f"The current time in {location} is {current_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}."
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Could not find timezone for {location}. Please provide a valid city or region name."
    except Exception as e:
        return f"An error occurred while getting time for {location}: {e}"

tools = [
    create_note,
    update_note,
    list_notes,
    read_note,
    StructuredTool.from_function(scheduler.schedule_job),
    StructuredTool.from_function(scheduler.get_dashboard_summary),
    get_current_time # Add the real get_current_time tool
]
llm_with_tools = llm.bind_tools(tools)

# Load system prompt
with open("system_prompt.md", "r") as f:
    SYSTEM_PROMPT = f.read()

# --- Define Graph State ---
# This defines the state of our graph, which will be passed between nodes.
# 'messages' is annotated to automatically append new messages.
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    dashboard_context: str # For Tier 1 context
    conditional_briefing: str # For Tier 2 context
    user_prompt: str # The raw user input

# --- Define Nodes ---

def build_context_node(state: AgentState) -> dict:
    """Builds the dashboard context (Tier 1) and potentially conditional briefing (Tier 2)."""
    # Tier 1: Unconditional Dashboard
    dashboard = build_dashboard_context(scheduler) # Pass scheduler instance
    
    # Tier 2: Conditional Briefing (Placeholder for now, will be expanded)
    # For now, we'll keep it simple. In future, this would involve RAG or other logic.
    conditional_briefing = ""

    return {
        "dashboard_context": dashboard,
        "conditional_briefing": conditional_briefing,
        "user_prompt": state.get("user_prompt", "") # Preserve user_prompt
    }

def call_llm_node(state: AgentState) -> dict:
    """Invokes the LLM with the combined context and messages."""
    messages = state["messages"]
    dashboard_context = state.get("dashboard_context", "")
    conditional_briefing = state.get("conditional_briefing", "")
    user_prompt = state.get("user_prompt", "")

    # Construct the full prompt for the LLM
    full_prompt_messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Dashboard Context:\n{dashboard_context}\n\nConditional Briefing:\n{conditional_briefing}\n\nUser Request: {user_prompt}")
    ] + messages # Append existing messages

    response = llm_with_tools.invoke(full_prompt_messages)
    return {"messages": [response]}

# Node for tool execution
tool_execution_node = ToolNode(tools=tools)

# --- Build the LangGraph ---
graph_builder = StateGraph(AgentState)

# Add nodes to the graph
graph_builder.add_node("build_context", build_context_node)
graph_builder.add_node("call_llm", call_llm_node)
graph_builder.add_node("tool_executor", tool_execution_node)

# Set the entry point for the graph
graph_builder.set_entry_point("build_context")

# Define edges
graph_builder.add_edge("build_context", "call_llm")

# Define conditional edges from the LLM node:
# If the LLM calls a tool, route to the tool_executor.
# Otherwise, if the LLM provides a direct answer, end the graph.
graph_builder.add_conditional_edges(
    "call_llm",
    tools_condition,
    {"tools": "tool_executor", END: END} 
)

# After a tool is executed, return to the LLM to process the tool's output
graph_builder.add_edge("tool_executor", "call_llm")

# Compile the graph with a checkpointer for memory persistence
memory = InMemorySaver() # Using in-memory for this POC, can be replaced with persistent storage
agent_graph_app = graph_builder.compile(checkpointer=memory)

# --- Main Execution Block (for testing) ---
if __name__ == "__main__":
    print("Welcome to the LangGraph-powered AI agent. Simulating conversation...")
    thread_id = "main_conversation" # Using a fixed thread_id for this Proof-of-Concept

    simulated_inputs = [
        "Hello, what can you do?",
        "List all my notes.",
        "What is the current time in New York?",
        "Schedule a job to remind me to call mom tomorrow at 9 AM.",
        "What jobs are scheduled?",
        "exit" # Command to end the simulated conversation
    ]

    for user_input in simulated_inputs:
        print(f"\nUser: {user_input}") # Print user input for clarity
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Prepare inputs and configuration for the graph invocation
        # Pass the raw user input to the state for context building
        inputs = {"messages": [HumanMessage(content=user_input)], "user_prompt": user_input}
        config = {"configurable": {"thread_id": thread_id}}

        # Stream the response from the agent
        final_response_content = ""
        for s in agent_graph_app.stream(inputs, config):
            if "call_llm" in s:
                # Extract the LLM's message (which could be a direct answer or a tool call)
                last_message = s["call_llm"]["messages"][-1]
                if hasattr(last_message, 'content') and last_message.content:
                    final_response_content += last_message.content
                elif hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    # Indicate if the agent is using a tool
                    final_response_content += f"\n(Agent is using a tool: {last_message.tool_calls})\n"
            elif "tool_executor" in s:
                # Extract and display the tool's output
                tool_output = s["tool_executor"]["messages"][-1].content
                final_response_content += f"\n(Tool Output: {tool_output})\n"
        print(f"Agent: {final_response_content.strip()}")
