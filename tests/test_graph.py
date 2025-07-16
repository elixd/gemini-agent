import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool

from agent.graph import create_graph


@tool
def placeholder_shell_tool(command: str) -> str:
    """A placeholder tool that simulates running a shell command."""
    return f"output of '{command}'"


def test_graph_with_tool_call():
    """
    Tests that the graph correctly calls a tool and returns the result.
    """
    # 1. Define a mock LLM that returns a canned response.
    # This is a simple function that mimics the behavior of an LLM's invoke method.
    def mock_llm(messages, *args, **kwargs):
        # The first time it's called, it returns a tool call.
        # The second time, it returns a final answer.
        if len(messages) == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "tool_call_123",
                        "name": "placeholder_shell_tool",
                        "args": {"command": "ls -l"},
                    }
                ],
            )
        else:
            return AIMessage(content="Done.")

    # 2. Create the graph with the placeholder tool and the mock LLM
    tools = [placeholder_shell_tool]
    mock_llm_instance = type("MockLLM", (), {"invoke": staticmethod(mock_llm)})()
    graph = create_graph(mock_llm_instance, tools)

    # 3. Invoke the graph
    input_message = HumanMessage(content="Run the ls command")
    result = graph.invoke({"messages": [input_message]})

    # 4. Assert the output
    messages = result["messages"]
    assert len(messages) == 4  # HumanMessage, AIMessage(tool_call), ToolMessage, AIMessage(final)

    # Check the ToolMessage
    tool_message = messages[2]
    assert isinstance(tool_message, ToolMessage)
    assert tool_message.content == "output of 'ls -l'"
    assert tool_message.tool_call_id == "tool_call_123"

    # Check the final AI message
    final_message = messages[3]
    assert final_message.content == "Done."