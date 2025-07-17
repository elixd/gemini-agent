from functools import partial
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.state import AgentState

def agent_node(state, llm):
    """Invokes the LLM to get a response."""
    return {"messages": [llm.invoke(state["messages"])]}

def create_graph(llm, tools, checkpointer):
    """
    Creates the agent graph using the standard, cyclical tool-calling pattern.
    """
    builder = StateGraph(AgentState)

    builder.add_node("agent", partial(agent_node, llm=llm))
    builder.add_node("tools", ToolNode(tools))

    builder.set_entry_point("agent")
    builder.add_conditional_edges(
        "agent",
        tools_condition,
    )
    builder.add_edge("tools", "agent")

    # The graph is compiled with the checkpointer
    return builder.compile(checkpointer=checkpointer)
