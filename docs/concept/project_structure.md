# Project Structure

This document outlines the proposed directory structure for the agent project. The structure is designed to be simple, comprehensible, and extensible, following the principles in `programming_approach.md`.

## Root Directory

```
.
├── agent/
│   ├── __init__.py
│   ├── graph.py
│   ├── state.py
│   └── tools/
│       ├── __init__.py
│       ├── file_system.py
│       ├── shell.py
│       ├── web.py
│       └── memory.py
├── core/
│   ├── __init__.py
│   ├── persistent_memory.py
│   └── models.py
├── tests/
│   └── ...
├── main.py
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

## Component Descriptions

### `main.py`
The single, unambiguous entry point for the command-line application. It acts as the central orchestrator, responsible for:
- Importing all necessary components (state, tools, graph logic, memory functions).
- Composing them into a runnable agent.
- Executing the main application loop for the CLI.

### `agent/`
A Python package containing the core components of the agent's "brain."
-   `graph.py`: Defines the LangGraph state machine, including nodes, edges, and conditional logic.
-   `state.py`: Defines the `AgentState` TypedDict for the graph.
-   `tools/`: A sub-package containing all the agent's capabilities, with each module grouping related tool functions.

### `core/`
A package for foundational services that are not part of the core agent logic but are essential for the application.
-   `persistent_memory.py`: Manages the agent's long-term "Persistent Memory" by reading from and writing to a local JSON file.
-   `models.py`: Configures and initializes the language models used by the agent.

### `tests/`
Contains all tests for the project.
