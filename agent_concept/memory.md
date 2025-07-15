# Agent Memory Architecture

The agent's memory is not a single entity but a sophisticated, layered system. It is designed to provide the Language Model with the maximum relevant context for any given task. This architecture combines immutable core instructions, session-specific conversation history, and persistent user-specific facts.

## Layer 1: Foundational Memory (Core Identity)

This is the agent's "constitution" or "firmware." It's a static, unchangeable set of instructions that defines its purpose, capabilities, constraints, and personality.

-   **Implementation:** This is the **System Prompt**.
-   **Characteristics:**
    -   **Immutable:** It does not change during a conversation.
    -   **Global:** It is present in every single request sent to the LLM.
    -   **Authoritative:** It provides the fundamental rules that govern all agent behavior.
-   **Content:** Includes core mandates, operational guidelines, tool usage protocols, and safety constraints.

## Layer 2: Working Memory (Conversation History)

This is the most active and dynamic layer of memory. It is the complete, ordered record of the current interaction session.

-   **Implementation:** A list of messages managed by the LangGraph state, associated with a session `thread_id`.
-   **Characteristics:**
    -   **Volatile but Persistent (Session-wise):** It grows with each turn in a conversation and is saved between turns using a checkpointer. It is cleared or archived when a new session begins.
    -   **Chronological:** It maintains the precise order of events.
    -   **Comprehensive:** It includes:
        -   User messages (`HumanMessage`)
        -   Agent's responses (`AIMessage`)
        -   Agent's decisions to use tools (`tool_calls`)
        -   The results of those tool executions (`ToolMessage`)
-   **Function:** This layer provides the immediate context for the LLM's reasoning. By seeing the full back-and-forth, the agent can understand follow-up questions, refer to previous statements, and track the progress of a multi-step task.

## Layer 3: Persistent Memory (Learned Facts)

This layer allows the agent to retain specific pieces of information across different sessions, providing personalization and long-term context.

-   **Implementation:** A dedicated `save_memory` tool connected to a persistent key-value store. The `core/persistent_memory.py` module will manage this, reading from and writing to a local JSON file (e.g., `memory.json`).
-   **Characteristics:**
    -   **Explicitly Written:** Memory is only added to this layer when the user explicitly instructs the agent to remember something via the `save_memory` tool. The agent does not learn facts passively.
    -   **Persistent:** Stored indefinitely, independent of any single conversation.
    -   **Injected into Prompt:** All relevant facts from this layer are retrieved and inserted into a special section of the prompt for every turn, making them available to the LLM alongside the foundational and working memory.
-   **Function:** This allows the agent to remember user preferences ("I prefer tabs over spaces"), project-specific details ("The database schema is in `schema.sql`"), or any other fact the user deems important.

## Synthesis: The "Full Prompt"

For any given turn, these three layers are synthesized into a single, comprehensive prompt that is sent to the LLM. The agent's effective "memory" at the moment of decision-making is the entirety of this context. It does not have a continuous stream of consciousness outside of this prompt.

This layered approach ensures the agent is:
-   **Grounded:** By its foundational rules.
-   **Context-Aware:** By the immediate conversation history.
-   **Personalized:** By the long-term learned facts.