import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent

load_dotenv()


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from custom_tools import create_note_tool, read_note_tool, schedule_job_tool, remove_job_tool, get_scheduled_jobs_tool
from dashboard import build_dashboard_context

# --- Configuration ---
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)

# --- Define Tools ---
tools = [create_note_tool, read_note_tool, schedule_job_tool, remove_job_tool, get_scheduled_jobs_tool]

# --- Define the agent prompt ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a proactive, context-aware personal AI assistant.\n\n# World Awareness Dashboard\n{dashboard}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# --- Create the Agent ---
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def run_agent(user_input, scheduler, chat_history):
    dashboard = build_dashboard_context(scheduler)
    return agent_executor.invoke({"input": user_input, "dashboard": dashboard, "chat_history": chat_history})