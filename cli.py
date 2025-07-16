import argparse
import uuid
import os
import platform
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

from agent.graph import create_graph
from agent.tools.shell import run_shell_command
from agent.tools.file_system import list_directory, read_file, write_file
from agent.tools.memory import save_memory
from agent.tools.web import google_web_search
from core.models import get_model
from core.persistent_memory import read_memory, write_memory


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
    
    if "messages" in output:
        for message in output["messages"]:
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
    load_dotenv()

    tools = [run_shell_command, list_directory, read_file, write_file, save_memory, google_web_search]
    llm = get_model().bind_tools(tools)
    graph = create_graph(llm, tools)

    session_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}

    system_prompt_template = assemble_system_prompt()

    # --- Gather and Inject Contextual Information ---
    cwd = os.getcwd()
    os_name = platform.system()
    current_date = datetime.now().strftime("%Y-%m-%d")
    directory_listing = list_directory.invoke({"path": os.getcwd()})
    
    system_prompt = system_prompt_template.replace("{{date}}", current_date)
    system_prompt = system_prompt.replace("{{os}}", os_name)
    system_prompt = system_prompt.replace("{{cwd}}", cwd)
    system_prompt = system_prompt.replace("{{directory_listing}}", directory_listing)

    memory = read_memory()
    if memory:
        system_prompt += f"\n\n# User-Specific Memory\n" + "\n".join(f"- {fact}" for fact in memory)

    messages = [SystemMessage(content=system_prompt)]

    print("Welcome to the interactive CLI agent. Type 'exit' or 'quit' to end the session.")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ["exit", "quit"]:
                break

            messages.append(HumanMessage(content=user_input))
            
            # --- Stream and Print Each Step of the Graph Execution ---
            print("\n--- Agent Run Start ---")
            for event in graph.stream({"messages": messages}, config):
                for node, output in event.items():
                    print_compact_output(node, output)
                    if "messages" in output:
                        messages.extend(output["messages"])
            print("\n--- Agent Run End ---")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("\nExiting.")


if __name__ == "__main__":
    main()
