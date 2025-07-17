import uuid
import os
import platform
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


def print_compact_output(node, output):
    """Prints the output in a compact, technical format."""
    print(f"[Node: {node}]")
    
    # With "updates" stream mode, the output is a dictionary where keys are the
    # state keys that have been updated. We are interested in "messages".
    if "messages" in output:
        messages = output["messages"]
        for message in messages:
            if isinstance(message, AIMessage):
                if message.tool_calls:
                    print("  -> Tool Call:")
                    for tool_call in message.tool_calls:
                        print(f"     - {tool_call['name']}")
                        for arg, value in tool_call['args'].items():
                            print(f"       - {arg}: {value}")
                else:
                    print(f"  -> Final Answer: \"{message.content}\"")
            elif isinstance(message, ToolMessage):
                print(f"  -> Tool Result: {message.name}")
                print(f"     - STDOUT:\n{message.content}")

def main():
    """The main entry point for the CLI application."""
    load_dotenv(override=True)

    tools = [run_shell_command, list_directory, read_file, write_file, save_memory, google_web_search]
    llm = get_model().bind_tools(tools)
    
    # Add the checkpointer during compilation
    memory = MemorySaver()
    graph = create_graph(llm, tools, checkpointer=memory)

    session_id = "interactive-session"
    config = {"configurable": {"thread_id": session_id}}

    # --- System Prompt Setup ---
    conversation_history = memory.get(config)
    if not conversation_history:
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
        graph.update_state(config, {"messages": initial_messages})

    print("Welcome to the interactive CLI agent. Type 'exit' or 'quit' to end the session.")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ["exit", "quit"]:
                break

            new_message = HumanMessage(content=user_input)
            
            print("\n--- Agent Run Start ---")
            # Use "updates" stream mode to get only the changed state at each step
            for event in graph.stream({"messages": [new_message]}, config, stream_mode="updates"):
                for node, output in event.items():
                    print_compact_output(node, output)
            print("\n--- Agent Run End ---")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("\nExiting.")

if __name__ == "__main__":
    main()
