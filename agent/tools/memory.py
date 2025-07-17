from langchain_core.tools import tool
from core.persistent_memory import read_memory, write_memory

@tool
def save_memory(fact: str) -> str:
    """
    Saves a specific fact to the user's long-term memory file.
    Use this when the user explicitly asks to remember something.
    The fact should be a concise, self-contained statement.
    """
    try:
        facts = read_memory()
        if fact not in facts:
            facts.append(fact)
            write_memory(facts)
        return "Fact saved successfully."
    except Exception as e:
        return f"Error saving fact: {e}"
