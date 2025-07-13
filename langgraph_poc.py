import os
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # Load environment variables from .env file

# Ensure OPENROUTER_API_KEY is set
if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("OPENROUTER_API_KEY environment variable not set. Please set it in your .env file or environment.")

# Initialize the LLM with OpenRouter configuration
llm = ChatOpenAI(
    model="google/gemini-2.5-flash-preview",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
)

# --- Define Tools ---
@tool
def get_current_time(location: str) -> str:
    """Get the current time in a specific location."""
    # In a real application, this would call an external API or use a more robust time library
    return f"The current time in {location} is 10:30 AM (placeholder)."

# List of tools available to the LLM
tools = [get_current_time]
llm_with_tools = llm.bind_tools(tools)

# --- Define Graph State ---
# This defines the state of our graph, which will be passed between nodes.
# 'messages' is annotated to automatically append new messages.
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# --- Define Nodes ---
# Node for LLM interaction
def call_llm(state: AgentState) -> dict:
    """Invokes the LLM with the current messages and returns its response."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Node for tool execution
# The ToolNode automatically executes tools called by the LLM
tool_node = ToolNode(tools=tools)

# --- Build the LangGraph ---
graph_builder = StateGraph(AgentState)

# Add nodes to the graph
graph_builder.add_node("llm_node", call_llm)
graph_builder.add_node("tool_node", tool_node)

# Set the entry point for the graph
graph_builder.set_entry_point("llm_node")

# Define conditional edges:
# If the LLM calls a tool, route to the tool_node.
# Otherwise, if the LLM provides a direct answer, end the graph.
graph_builder.add_conditional_edges(
    "llm_node",
    tools_condition,
    {"tools": "tool_node", END: END} # "tools" is the key returned by tools_condition when a tool is called
)

# After a tool is executed, return to the LLM to process the tool's output
graph_builder.add_edge("tool_node", "llm_node")

# Compile the graph with a checkpointer for memory persistence
memory = InMemorySaver() # Using in-memory for this POC, can be replaced with persistent storage
app = graph_builder.compile(checkpointer=memory)

# --- Run the Conversational Agent ---
if __name__ == "__main__":
    print("Welcome to the LangGraph conversational agent. Simulating conversation...")
    # Using a fixed thread_id for this Proof-of-Concept to maintain conversation history
    thread_id = "1" 

    # Predefined inputs to simulate a conversation
    simulated_inputs = [
        "Hello, how are you?",
        "What time is it in London?",
        "Do you remember my previous question?",
        "What about Tokyo?",
        "exit" # Command to end the simulated conversation
    ]

    for user_input in simulated_inputs:
        print(f"\nUser: {user_input}") # Print user input for clarity
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Prepare inputs and configuration for the graph invocation
        inputs = {"messages": [("user", user_input)]}
        config = {"configurable": {"thread_id": thread_id}}

        # Stream the response from the agent
        final_response_content = ""
        for s in app.stream(inputs, config):
            if "llm_node" in s:
                # Extract the LLM's message (which could be a direct answer or a tool call)
                last_message = s["llm_node"]["messages"][-1]
                if hasattr(last_message, 'content') and last_message.content:
                    final_response_content += last_message.content
                elif hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    # Indicate if the agent is using a tool
                    final_response_content += f"\n(Agent is using a tool: {last_message.tool_calls})\n"
            elif "tool_node" in s:
                # Extract and display the tool's output
                tool_output = s["tool_node"]["messages"][-1].content
                final_response_content += f"\n(Tool Output: {tool_output})\n"
        print(f"Agent: {final_response_content.strip()}")

