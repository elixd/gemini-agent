from functools import partial
from typing import Literal

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END

from agent.state import AgentState


def call_model(state: AgentState, llm):
    """This node invokes the LLM and returns its response."""
    return {"messages": [llm.invoke(state["messages"])]}


def call_tool(state: AgentState, tools):
    """
    This node executes the tools requested by the model.
    """
    last_message = state["messages"][-1]
    tool_messages = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_to_run = next(t for t in tools if t.name == tool_name)
        result = tool_to_run.invoke(tool_call["args"])
        tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
    return {"messages": tool_messages}


def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    """
    This is the conditional edge. It checks the last message in the state for tool calls.
    """
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return "__end__"


def create_graph(llm, tools):
    """
    Creates the agent graph using the standard, cyclical tool-calling pattern.
    """
    builder = StateGraph(AgentState)

    # Define the nodes
    builder.add_node("model", partial(call_model, llm=llm))
    builder.add_node("tools", partial(call_tool, tools=tools))

    # Define the edges
    builder.add_edge(START, "model")
    builder.add_conditional_edges(
        "model",
        should_continue,
        {"tools": "tools", "__end__": END},
    )
    builder.add_edge("tools", "model")

    # Compile the graph
    return builder.compile()