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
from agent.tools.shell import run_shell_command
from agent.tools.file_system import list_directory, read_file, write_file
from agent.tools.memory import save_memory
from agent.tools.web import google_web_search
from core.models import get_model
from core.persistent_memory import read_memory


def assemble_system_prompt():
    """
    Assembles the full system prompt from the components in the prompt_components directory.
    """
    prompt_dir = "core/prompt_components"
    prompt_files = sorted([f for f in os.listdir(prompt_dir) if f.endswith(".md")])
    
    full_prompt = ""
    for file_name in prompt_files:
        with open(os.path.join(prompt_dir, file_name), "r") as f:
            full_prompt += f.read() + "\n\n"
            
    return full_prompt.strip()


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
  python3 cli.py

  # Execute a single command
  python3 cli.py -c "What is the current directory?"
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
    args = parser.parse_args()

    load_dotenv(override=True)

    tools = [run_shell_command, list_directory, read_file, write_file, save_memory, google_web_search]
    llm = get_model().bind_tools(tools)
    
    memory = MemorySaver()
    graph = create_graph(llm, tools, checkpointer=memory)

    session_id = "default-session"
    config = {"configurable": {"thread_id": session_id}}

    # Determine the initial message list
    is_new_conversation = not memory.get(config)
    if is_new_conversation:
        print("Starting a new conversation. Assembling system prompt...")
        system_prompt_template = assemble_system_prompt()
        cwd = os.getcwd()
        os_name = platform.system()
        current_date = datetime.now().strftime("%Y-%m-%d")
        try:
            directory_listing = list_directory.invoke({"path": os.getcwd()})
        except Exception as e:
            directory_listing = f"Could not list directory: {e}"
        system_prompt = system_prompt_template.replace("{{date}}", current_date)
        system_prompt = system_prompt.replace("{{os}}", os_name)
        system_prompt = system_prompt.replace("{{cwd}}", cwd)
        system_prompt = system_prompt.replace("{{directory_listing}}", directory_listing)
        facts = read_memory()
        if facts:
            system_prompt += f"\n\n# User-Specific Memory\n" + "\n".join(f"- {fact}" for fact in facts)
        initial_messages = [SystemMessage(content=system_prompt)]
    else:
        initial_messages = []

    if args.command:
        print_input_header()
        print(f"> {args.command}")
        print_input_footer()
        
        new_message = HumanMessage(content=args.command)
        
        # For verbose mode, construct the payload manually to ensure accuracy
        if args.verbose:
            current_state = memory.get(config)
            history = (current_state.get('messages', []) if current_state else initial_messages)
            print_payload(history + [new_message])

        # Update the state with the initial messages if it's a new conversation
        if is_new_conversation:
            graph.update_state(config, {"messages": initial_messages})

        for event in graph.stream({"messages": [new_message]}, config, stream_mode="updates"):
            for node, output in event.items():
                print_compact_output(node, output)
    else:
        print("Welcome to the interactive CLI agent. Type 'exit' or 'quit' to end the session.")
        
        # On the first run in interactive mode, save the initial state
        if is_new_conversation:
            graph.update_state(config, {"messages": initial_messages})

        while True:
            try:
                print_input_header()
                user_input = input("> ")
                print_input_footer()
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                new_message = HumanMessage(content=user_input)

                if args.verbose:
                    current_state = memory.get(config)
                    history = current_state.get('messages', [])
                    print_payload(history + [new_message])

                for event in graph.stream({"messages": [new_message]}, config, stream_mode="updates"):
                    for node, output in event.items():
                        print_compact_output(node, output)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}")
        print("\nExiting.")

if __name__ == "__main__":
    main()