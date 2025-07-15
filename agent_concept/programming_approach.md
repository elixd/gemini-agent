# Programming Approach

This document outlines the core programming philosophy and architectural principles for this project. The primary goal is to create a codebase that is clean, highly testable, and easy to reason about.

## 1. Functional and Composable Design

We will prioritize a functional approach over a class-based one for the core agent logic.

-   **Nodes as Functions:** LangGraph nodes will be implemented as simple functions. Each function will take the current state as input and return a dictionary of updates, avoiding hidden side effects.
-   **Composition over Inheritance:** The agent's behavior will be built by composing these smaller functions together within the graph, rather than inheriting from a large, monolithic `Agent` class.

## 2. Dependency Injection for Testability

This is the most critical principle for ensuring our code is testable. The components of our application will not create their own dependencies; they will receive them as arguments.

-   **The Rule:** A function or module that needs a "service" (like an LLM, a tool, or a database connection) must accept it as a parameter.
-   **Why:** This allows us to "inject" a real dependency for the running application, but a fake (mock) dependency during testing. This avoids the need for complex patching and makes our tests simple, robust, and easy to read. For concrete examples, refer to the project's test files.

## 3. Clear Separation of Concerns

Even within our simple structure, we will maintain a logical separation of responsibilities to keep the codebase organized and predictable.

-   **`state.py`:** Defines the data structure (the "what").
-   **`graph.py`:** Defines the control flow (the "how").
-   **`tools/`:** A package containing all agent capabilities.
-   **`core/`:** Contains foundational services like persistence.
-   **`main.py`:** Orchestrates the assembly and execution of the application.

## 4. Observability as a Core Feature

Understanding the agent's internal reasoning is critical for debugging and development. We will build in a robust, optional logging system from the start.

-   **Unified Logging:** We will use Python's built-in `logging` module to record key events, such as full LLM prompts, raw LLM responses, tool calls, and tool results.
-   **Verbose Flag:** The CLI (`main.py`) will include a `--verbose` or `--debug` flag. When enabled, this flag will print the detailed event log to the console, allowing us to "peel back the abstraction" and see the agent's step-by-step reasoning. When disabled, the interface will remain a clean, simple chat.
-   **Testability:** The same logging system will be available during automated tests, which can be configured to show verbose output on test failure, aiding in debugging.
