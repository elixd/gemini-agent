import argparse
import uuid
import os
import platform
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver

from agent.graph import create_graph
from agent.composition import TOOLS, assemble_system_prompt
from core.models import get_model


def print_input_header():
    """Prints the header for human input."""
    print("\n========[Human Input]=========")

def print_input_footer():
    """Prints the footer for human input."""
    print("==============================")

def print_agent_answer(text: str):
    """Formats and prints the agent's final answer."""
    if not text:
        return
    # Prefix each line with three spaces
    formatted = "\n".join([f"   {line}" for line in text.splitlines()])
    print(formatted)

def print_tool_call(tool_call):
    """Prints a formatted tool call."""
    # Recreate the command string with parameters
    args_str = " ".join([f"{k}={v}" for k, v in tool_call['args'].items()])
    print(f"   -> Tool Call: {tool_call['name']} {args_str}")

def print_tool_result(tool_name: str, stdout: str):
    """Formats and prints the stdout of a tool."""
    if not stdout:
        return
    # Prefix each line with the box-drawing character
    formatted = "\n".join([f"│  {line}" for line in stdout.splitlines()])
    print(f"\n{formatted}\n")

def print_compact_output(node, output):
    """Prints the output in a compact, technical format."""
    print(f"\n[Node: {node}]")
    
    if "messages" in output:
        for message in output["messages"]:
            if isinstance(message, AIMessage):
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        print_tool_call(tool_call)
                else:
                    print_agent_answer(message.content)
            elif isinstance(message, ToolMessage):
                print_tool_result(message.name, message.content)

def print_payload(messages_to_send):
    """Prints the full payload to be sent to the model."""
    print("\n--- Payload to be sent to the model ---")
    serializable_messages = [msg.to_json() for msg in messages_to_send]
    print(json.dumps(serializable_messages, indent=2))
    print("-----------------------------------------")

def main():
    """The main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="A conversational CLI agent that can use tools to perform tasks.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  # Run in interactive mode
  python3 interfaces/cli.py

  # Execute a single command
  python3 interfaces/cli.py -c "What is the current directory?"
"""
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output, including the JSON payload sent to the model."
    )
    parser.add_argument(
        "-c", "--command", 
        type=str, 
        help="Execute a single command and exit. If not provided, the agent will start in interactive mode."
    )
    parser.add_argument(
        '--test-sequence',
        nargs='+',
        help="Execute a sequence of commands in a single session for testing."
    )
    args = parser.parse_args()

    load_dotenv(override=True);

    # --- Agent Assembly ---
    # This is now transparent and explicit, following the "Shared Core" approach.
    # Any interface can replicate this logic to get a fully-formed agent.
    llm = get_model().bind_tools(TOOLS)
    memory = MemorySaver()
    graph = create_graph(llm, TOOLS, checkpointer=memory)
    # --- End of Assembly ---

    session_id = "default-session"
    config = {"configurable": {"thread_id": session_id}}

    # Determine the initial message list
    current_state = memory.get(config)
    is_new_conversation = not current_state
    
    if is_new_conversation:
        print("Starting a new conversation. Assembling system prompt...")
        system_prompt = assemble_system_prompt()
        initial_messages = [SystemMessage(content=system_prompt)]
        graph.update_state(config, {"messages": initial_messages})
    else:
        initial_messages = []

    # The checkpointer handles state. We simply send the new message.
    if args.test_sequence:
        for i, command in enumerate(args.test_sequence):
            print_input_header()
            print(f"Step {i+1}: > {command}")
            print_input_footer()
            
            for event in graph.stream({"messages": [HumanMessage(content=command)]}, config, stream_mode="updates"):
                for node, output in event.items():
                    print_compact_output(node, output)

    elif args.command:
        print_input_header()
        print(f"> {args.command}")
        print_input_footer()
        
        for event in graph.stream({"messages": [HumanMessage(content=args.command)]}, config, stream_mode="updates"):
            for node, output in event.items():
                print_compact_output(node, output)
    else:
        print("Welcome to the interactive CLI agent. Type 'exit' or 'quit' to end the session.")
        
        while True:
            try:
                print_input_header()
                user_input = input("> ")
                print_input_footer()
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                for event in graph.stream({"messages": [HumanMessage(content=user_input)]}, config, stream_mode="updates"):
                    for node, output in event.items():
                        print_compact_output(node, output)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}")
        print("\nExiting.")

if __name__ == "__main__":
    main()
