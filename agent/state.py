from typing import Annotated, List

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """The state of our agent."""

    messages: Annotated[list, add_messages]
    memory: List[str]
