
"""
This module defines the core, reusable components of the agent.

Interfaces (like the CLI or a Telegram bot) can import these components
to build a complete agent instance. This promotes transparency and avoids
code duplication.
"""
import os
import platform
from datetime import datetime

from agent.tools.shell import run_shell_command
from agent.tools.file_system import (
    list_directory, 
    read_file, 
    write_file, 
    search_file_content, 
    glob, 
    replace, 
    read_many_files
)
from agent.tools.memory import save_memory
from agent.tools.web import google_web_search
from core.persistent_memory import read_memory

# A constant list of all tools available to the agent.
# This makes it easy for any interface to create an agent with the same capabilities.
TOOLS = [
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

def assemble_system_prompt():
    """
    Assembles the full system prompt from the components in the prompt_components directory,
    injecting dynamic information like the current date, OS, and working directory.
    
    This function ensures that any interface starting the agent will get the exact same,
    up-to-date system prompt.
    """
    prompt_dir = "core/prompt_components"
    prompt_files = sorted([f for f in os.listdir(prompt_dir) if f.endswith(".md")])
    
    full_prompt = ""
    for file_name in prompt_files:
        with open(os.path.join(prompt_dir, file_name), "r") as f:
            full_prompt += f.read() + "\n\n"
            
    system_prompt_template = full_prompt.strip()

    # Inject dynamic information
    cwd = os.getcwd()
    os_name = platform.system()
    current_date = datetime.now().strftime("%Y-%m-%d")
    try:
        # Use the tool directly to get the initial directory listing
        directory_listing_output = list_directory.invoke({"path": os.getcwd()})
    except Exception as e:
        directory_listing_output = f"Could not list directory: {e}"

    system_prompt = system_prompt_template.replace("{{date}}", current_date)
    system_prompt = system_prompt.replace("{{os}}", os_name)
    system_prompt = system_prompt.replace("{{cwd}}", cwd)
    system_prompt = system_prompt.replace("{{directory_listing}}", directory_listing_output)
    
    # Add user-specific memories
    facts = read_memory()
    if facts:
        system_prompt += f"\n\n# User-Specific Memory\n" + "\n".join(f"- {fact}" for fact in facts)
        
    return system_prompt
