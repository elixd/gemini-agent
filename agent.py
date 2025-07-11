
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from functions import create_note, update_note, list_notes, read_note
from scheduler import Scheduler

load_dotenv()

# 1. Define the Model
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)

from langchain.tools import StructuredTool

# 2. Define the Tools
scheduler = Scheduler('schedule.json')
tools = [
    create_note,
    update_note,
    list_notes,
    read_note,
    StructuredTool.from_function(scheduler.schedule_job),
    StructuredTool.from_function(scheduler.get_dashboard_summary),
]

# 3. Define the Prompt
with open("system_prompt.md", "r") as f:
    system_prompt = f.read()

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. Create the Agent Executor
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
)
