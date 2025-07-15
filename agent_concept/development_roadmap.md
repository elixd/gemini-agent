# Development Roadmap

This document outlines the iterative, step-by-step plan for building the agent. Our core strategy is to build and test one piece of functionality at a time, ensuring each part is working perfectly before moving to the next.

## Phase 1: The Foundation (The "Echo" Agent)

The first goal is to create the simplest possible agent that proves our basic project structure is wired correctly.

1.  **Setup Project Structure:** Create the directories and files outlined in `project_structure.md`.
2.  **Define State:** Implement the initial `AgentState` in `agent/state.py`.
3.  **Create Echo Graph:** In `agent/graph.py`, define a graph with a single node that simply takes the user's input and returns it.
4.  **Build Main Orchestrator:** In `main.py`, write the code to assemble the echo graph and run the main CLI loop.
5.  **Test:** Manually run `main.py` and confirm that it echoes user input.

*At the end of this phase, we will have a working, runnable application, albeit a very simple one.*

## Phase 2: Incremental Tool Integration

This phase will be a repeating cycle where we add one new capability (or a small group of related capabilities) at a time.

### The Strategy: A Three-Step Cycle for Each Tool

For each new tool, we will follow a rigorous three-step process to ensure both our code logic and the agent's AI behavior are correct.

1.  **Test the Graph with a Placeholder:** First, we write an integration test for the graph. This test uses a **mock LLM** and a simple, hardcoded **placeholder tool**. This proves that the graph's control flow can handle the new tool *before* we write the tool's actual logic.

2.  **Implement and Unit-Test the Real Tool:** Second, we implement the real tool in its appropriate module within `agent/tools/`. We will write focused unit tests for this tool, mocking any external dependencies (like web APIs or the file system). This proves the tool's internal logic is correct.

3.  **Manually Verify with a Real LLM:** Finally, with the automated tests passing, we run the main application (`main.py`) connected to a **real LLM**. We then interact with the agent from the command line to confirm that the LLM is "smart" enough to choose and use the new tool correctly in a real-world scenario. This step is crucial for prompt engineering and validating the agent's practical usefulness.

### The Implementation Order

We will implement tools in the following logical order to build up the agent's capabilities:

1.  **Shell Command:** Implement and integrate the `run_shell_command` tool. This provides a powerful, general-purpose capability early on.
2.  **File System I/O:** Implement and integrate the core file system tools (`read_file`, `write_file`, `list_directory`).
3.  **Persistent Memory:** Implement the `save_memory` tool and the `core/persistent_memory.py` logic. This will allow the agent to learn.
4.  **Web Search:** Implement and integrate the `google_web_search` tool. This gives the agent access to external knowledge.
5.  **Advanced File Tools:** Implement the remaining file tools like `replace`, `search_file_content`, etc.

## Phase 3 and Beyond

Once the core toolset is in place and tested, future phases will involve:
-   Adding more complex tools (e.g., database interaction, email).
-   Refining the system prompt and agent's reasoning abilities.
-   (If desired) Refactoring to add new interfaces, such as the Telegram bot.

A Note on Observability: The `--verbose` output mode in the CLI is considered a core feature for development, debugging, and advanced use. It will be maintained throughout the project's lifecycle and will not be removed, even as the application matures.
