
"""
This module contains the factory function for creating the agent graph.
"""
import os
import platform
from datetime import datetime

from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from agent.graph import create_graph
from agent.tools.shell import run_shell_command
from agent.tools.file_system import list_directory, read_file, write_file, search_file_content, glob, replace, read_many_files
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


def create_agent():
    """
    Factory function to create the conversational agent graph.
    
    Returns:
        A tuple containing the compiled graph and the memory saver.
    """
    tools = [
        run_shell_command, 
        list_directory, 
        read_file, 
        write_file, 
        save_memory, 
        google_web_search,
        search_file_content,
        glob,
        replace,
        read_many_files
    ]
    llm = get_model().bind_tools(tools)
    
    memory = MemorySaver()
    graph = create_graph(llm, tools, checkpointer=memory)
    
    return graph, memory

def get_initial_messages(memory, config):
    """
    Determines the initial message list based on conversation history.
    """
    is_new_conversation = not memory.get(config)
    if not is_new_conversation:
        return []

    print("Starting a new conversation. Assembling system prompt...")
    system_prompt_template = assemble_system_prompt()
    cwd = os.getcwd()
    os_name = platform.system()
    current_date = datetime.now().strftime("%Y-%m-%d")
    try:
        # Using the tool's invoke method directly for initial setup
        directory_listing_output = list_directory.invoke({"path": os.getcwd()})
    except Exception as e:
        directory_listing_output = f"Could not list directory: {e}"

    system_prompt = system_prompt_template.replace("{{date}}", current_date)
    system_prompt = system_prompt.replace("{{os}}", os_name)
    system_prompt = system_prompt.replace("{{cwd}}", cwd)
    system_prompt = system_prompt.replace("{{directory_listing}}", directory_listing_output)
    
    facts = read_memory()
    if facts:
        system_prompt += f"\n\n# User-Specific Memory\n" + "\n".join(f"- {fact}" for fact in facts)
        
    return [SystemMessage(content=system_prompt)]

