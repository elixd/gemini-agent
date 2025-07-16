import json
import os

MEMORY_FILE = "memory.json"


def read_memory() -> list[str]:
    """
    Reads the list of facts from the memory file.
    Returns an empty list if the file doesn't exist.
    """
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def write_memory(facts: list[str]):
    """
    Writes the list of facts to the memory file.
    """
    with open(MEMORY_FILE, "w") as f:
        json.dump(facts, f, indent=2)
