import json

from langchain_core.tools import tool
from core.persistent_memory import read_memory, write_memory

@tool
def save_memory(fact: str) -> str:
    """
    Saves a specific fact to the user's long-term memory file.
    Use this when the user explicitly asks to remember something.
    The fact should be a concise, self-contained statement.
    """
    if not fact:
        return json.dumps({"success": False, "error": 'Parameter "fact" must be a non-empty string.'})
    try:
        facts = read_memory()
        if fact not in facts:
            facts.append(fact)
            write_memory(facts)
        return json.dumps({"success": True, "message": f'Okay, I\'ve remembered that: "{fact}"'})
    except Exception as e:
        return json.dumps({"success": False, "error": f"Error saving fact: {e}"})
