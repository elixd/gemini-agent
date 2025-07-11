import os
from langchain.tools import tool

NOTES_DIR = "notes"

if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

@tool
def create_note(topic: str) -> str:
    """Creates a new note file with the given topic. The topic should be a short, snake_cased string."""
    file_path = os.path.join(NOTES_DIR, f"{topic}.md")
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(f"# {topic.replace('_', ' ').title()}\n\n")
        return f"Note file ''{topic}.md'' created."
    else:
        return f"Note file ''{topic}.md'' already exists."

@tool
def list_notes() -> str:
    """Lists all available note files."""
    notes = os.listdir(NOTES_DIR)
    if not notes:
        return "No notes found."
    return "\n".join([f"- {note}" for note in notes])

@tool
def read_note(topic: str) -> str:
    """Reads the content of a specific note file."""
    file_path = os.path.join(NOTES_DIR, f"{topic}.md")
    if not os.path.exists(file_path):
        return f"Error: Note file ''{topic}.md'' not found."
    with open(file_path, 'r') as f:
        return f.read()

@tool
def update_note(topic: str, text: str) -> str:
    """Updates a note file with the given topic by appending text to it."""
    file_path = os.path.join(NOTES_DIR, f"{topic}.md")
    if not os.path.exists(file_path):
        return "Error: Note with that topic does not exist. You could create it first using the `create_note` tool."
    
    with open(file_path, 'a') as f:
        f.write(f"- {text}\n")
    return f"Note ''{topic}.md'' updated."
