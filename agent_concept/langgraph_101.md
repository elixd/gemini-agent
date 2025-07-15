# LangGraph 101: Core Concepts for Our Agent

This document provides the essential LangGraph concepts and patterns we will use to build our agent. It is the primary technical reference for implementing the graph structure.

## The Core Pattern: A Stateful Graph

Our agent's logic is built as a `StateGraph`, which is a state machine. The graph is composed of **nodes** (functions that do work) and **edges** (which connect the nodes).

### 1. Defining the State

The first step is to define the structure of the data that will be passed between the nodes. This is our agent's "state." We use a `TypedDict` for this. For our project, the state must contain a list of messages.

The `Annotated[list, add_messages]` syntax is a special reducer that tells LangGraph to *append* new messages to the list, rather than replacing it on each step.

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """The state of our agent."""
    messages: Annotated[list, add_messages]
```

### 2. Defining Tools

For the LLM to use our tools, we must define them as simple Python functions and decorate them with the `@tool` decorator from LangChain. This decorator automatically inspects the function's signature (argument names, type hints) and its docstring to make it available to the LLM.

-   The function's name becomes the tool's name.
-   The function's docstring becomes the tool's description, which the LLM uses to decide when to use it.
-   The function's arguments (with type hints) become the tool's arguments.

```python
from langchain_core.tools import tool

@tool
def read_file(absolute_path: str) -> str:
    """
    Reads and returns the full content of a specified file.
    The path must be an absolute path.
    """
    # ... implementation of the tool ...
    return content
```

These tool functions will be implemented in the `agent/tools/` directory and then collected into a list in `main.py` to be passed to the `ToolNode` and bound to the LLM.

### 3. Defining Nodes

A **node** is a function that performs an action. Every node receives the current `AgentState` as its only input and must return a dictionary where the keys match the keys in `AgentState`, containing the values to update.

Our primary node is the `chatbot` node, which calls the LLM.

```python
# llm_with_tools is our language model, configured with the tools it can use.
# This will be created in main.py and passed to the graph builder.

def chatbot_node(state: AgentState):
    """This node invokes the LLM."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}
```

### 4. Building the Graph

We initialize a `StateGraph` with our `AgentState` and add our nodes to it.

```python
graph_builder = StateGraph(AgentState)

# Add the chatbot node
graph_builder.add_node("chatbot", chatbot_node)
```

### 5. The Tool-Calling Loop

This is the central mechanism of our agent. It allows the `chatbot` node to request a tool, have it executed, and then receive the result to continue its reasoning.

**A. The `ToolNode`**
LangGraph provides a pre-built `ToolNode` that executes tool calls for us. We simply initialize it with our list of tool functions.

```python
from langgraph.prebuilt import ToolNode

# 'tools' is the list of our actual tool functions (e.g., read_file, run_shell_command)
# This will be created in main.py.
tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)
```

**B. Conditional Edges**
After the `chatbot` node runs, we need to decide where to go next.
- If the LLM asked to use a tool, we go to the `tool_node`.
- If the LLM responded directly, the turn is over, and we go to `END`.

We use a **conditional edge** for this. LangGraph provides a pre-built `tools_condition` function that handles this logic perfectly.

```python
from langgraph.prebuilt import tools_condition

# This creates the conditional branch.
graph_builder.add_conditional_edges(
    start_node="chatbot",
    condition=tools_condition,
    # The dictionary maps the condition's output (a string) to a destination node.
    # If the condition returns "tools", the graph goes to the "tools" node.
    # Otherwise, it goes to END.
    node_map={"tools": "tools", END: END}
)
```

**C. Completing the Loop**
After the `tool_node` runs, the result is appended to the state. We must then route control back to the `chatbot` node so it can process the tool's output.

```python
graph_builder.add_edge("tools", "chatbot")
```

### 6. Defining the Entry Point

We must explicitly tell the graph where to start.

```python
graph_builder.set_entry_point("chatbot")
```

### 7. Adding Memory (Persistence)

To enable conversational memory, we use a **checkpointer**. The checkpointer saves the state of the graph after every step.

For development, we will use the simple `MemorySaver`.

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
```

When we compile the graph, we attach the checkpointer.

```python
# This creates the final, runnable application.
graph = graph_builder.compile(checkpointer=memory)
```

To use the memory, every invocation of the graph must include a `thread_id` in its configuration. This `thread_id` represents a unique conversation.

```python
# This config must be passed with every call for a given conversation.
config = {"configurable": {"thread_id": "some-unique-conversation-id"}}

graph.invoke(
    {"messages": [("user", "Hello!")]},
    config=config
)
```

This is the complete set of core LangGraph concepts required to build our agent according to the project plan.
