The page, titled "3. Add memory", describes how to add persistent checkpointing to a LangGraph chatbot to enable multi-turn conversations.

Key steps include:
1.  **Creating a `MemorySaver` checkpointer**: This in-memory checkpointer is suitable for tutorials, but production applications would typically use `SqliteSaver` or `PostgresSaver` with a database.
2.  **Compiling the graph**: The graph is compiled with the `checkpointer` provided, which saves the state as the graph processes each node.
3.  **Interacting with the chatbot**: By providing a `thread_id` in the `config` when invoking the graph, LangGraph automatically saves and loads the state, allowing the chatbot to remember previous interactions.
4.  **Asking follow-up questions**: The tutorial demonstrates how the chatbot remembers the user's name across turns when the same `thread_id` is used, and how it "forgets" when a different `thread_id` is used.
5.  **Inspecting the state**: The `get_state(config)` method can be used to inspect the current state values, corresponding configuration, and the next node to process for a given thread.

The tutorial emphasizes that checkpointing in LangGraph is more powerful than simple chat memory, supporting complex state saving and resumption for error recovery, human-in-the-loop workflows, and time travel interactions.

Sources:
[1] 3. Add memory (https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/)