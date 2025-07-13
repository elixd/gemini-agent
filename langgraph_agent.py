import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.tools import tool
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.utils.function_calling import convert_to_openai_function

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

from custom_tools import create_note_tool, read_note_tool, schedule_job_tool, remove_job_tool, get_scheduled_jobs_tool
from dashboard import build_dashboard_context

load_dotenv()

# --- Configuration ---
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)

# --- Define Tools ---
langgraph_tools = [
    create_note_tool,
    read_note_tool,
    schedule_job_tool,
    remove_job_tool,
    get_scheduled_jobs_tool
]

# Convert tools to OpenAI functions for the LLM
functions = [convert_to_openai_function(t) for t in langgraph_tools]

# --- Define Agent State ---
class AgentState(TypedDict):
    input: str
    chat_history: List[BaseMessage]
    scheduler: object # Add scheduler to the state
    # The outcome of the agent's decision (tool call or final answer)
    agent_outcome: AgentAction | AgentFinish | None
    # Intermediate steps for tool execution
    intermediate_steps: Annotated[List[tuple[AgentAction, str]], operator.add]

# --- Define Nodes ---
def run_agent_node(state: AgentState):
    """
    Node that runs the LLM to decide the next action (tool call or final answer).
    """
    dashboard = build_dashboard_context(state["scheduler"])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a proactive, context-aware personal AI assistant.\n\n# World Awareness Dashboard\n{dashboard}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Bind tools to the LLM for function calling
    agent_runnable = prompt | llm.bind_tools(functions)

    # Invoke the LLM
    result = agent_runnable.invoke({
        "input": state["input"],
        "dashboard": dashboard,
        "chat_history": state["chat_history"],
        "agent_scratchpad": state["intermediate_steps"]
    })

    # Parse the result to determine if it's a tool call or a final answer
    if result.tool_calls:
        # It's a tool call
        # LangGraph expects AgentAction for tool calls
        tool_call = result.tool_calls[0] # Assuming single tool call for simplicity
        return {"agent_outcome": AgentAction(tool=tool_call.function.name, tool_input=tool_call.function.arguments, log=result.content)}
    else:
        # It's a final answer
        return {"agent_outcome": AgentFinish(return_values={"output": result.content}, log=result.content)}


def call_tool_node(state: AgentState):
    """
    Node that executes the tool based on the agent's decision.
    """
    agent_action = state["agent_outcome"]
    tool_name = agent_action.tool
    tool_args = agent_action.tool_input

    # Find the tool and execute it
    tool_output = "Tool not found or error during execution."
    for t in langgraph_tools:
        if t.name == tool_name:
            try:
                # Tool arguments are often strings, need to parse if they are JSON strings
                if isinstance(tool_args, str):
                    tool_args = json.loads(tool_args)
                tool_output = t.func(**tool_args)
            except Exception as e:
                tool_output = f"Error executing tool {tool_name}: {e}"
            break
    
    return {"intermediate_steps": [(agent_action, tool_output)]}

# --- Define the Graph ---
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_agent_node)
workflow.add_node("tools", call_tool_node)

workflow.set_entry_point("agent")

# Define the conditional edge from "agent"
workflow.add_conditional_edges(
    "agent",
    # Decide where to go next based on the agent's output
    lambda state: "tools" if isinstance(state["agent_outcome"], AgentAction) else "end",
    {
        "tools": "tools",
        "end": END
    }
)

workflow.add_edge("tools", "agent") # After tool execution, go back to the agent

compiled_app = workflow.compile()

# --- run_langgraph_agent function ---
def run_langgraph_agent(user_input, scheduler, chat_history):
    """
    Runs the LangGraph agent with the given user input, scheduler, and chat history.
    """
    # Initial state for the graph
    initial_state = {
        "input": user_input,
        "chat_history": chat_history,
        "scheduler": scheduler,
        "intermediate_steps": []
    }

    # Invoke the compiled graph
    # LangGraph's invoke returns the final state.
    final_state = compiled_app.invoke(initial_state)

    # Extract the final output
    if isinstance(final_state["agent_outcome"], AgentFinish):
        return final_state["agent_outcome"].return_values
    else:
        # If the agent didn't finish, it might be stuck or waiting for more input.
        # This could happen if the LLM doesn't return a tool call or a final answer.
        # For this simple example, let's return a generic message.
        return {"output": "Agent did not produce a final answer or got stuck."}