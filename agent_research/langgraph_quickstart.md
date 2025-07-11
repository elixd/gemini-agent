## LangGraph quickstart

This guide shows you how to set up and use LangGraph's **prebuilt**, **reusable** components, which are designed to help you construct agentic systems quickly and reliably.

## Prerequisites

Before you start this tutorial, ensure you have the following:

-   An [Anthropic](https://console.anthropic.com/settings/keys) API key

## 1. Install dependencies

If you haven't already, install LangGraph and LangChain:

```
pip install -U langgraph "langchain[anthropic]"
```

Info

LangChain is installed so the agent can call the [model](https://python.langchain.com/docs/integrations/chat/).

## 2. Create an agent

To create an agent, use [`create_react_agent`](https://langchain-ai.github.io/langgraph/reference/agents/#langgraph.prebuilt.chat_agent_executor.create_react_agent "            create_react_agent"):

API Reference: [create_react_agent](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)

```
from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:  # (1)!
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",  # (2)!
    tools=[get_weather],  # (3)!
    prompt="You are a helpful assistant"  # (4)!
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

1.  Define a tool for the agent to use. Tools can be defined as vanilla Python functions. For more advanced tool usage and customization, check the [tools](https://langchain-ai.github.io/langgraph/how-tos/tool-calling/) page.
2.  Provide a language model for the agent to use. To learn more about configuring language models for the agents, check the [models](https://langchain-ai.github.io/langgraph/agents/models/) page.
3.  Provide a list of tools for the model to use.
4.  Provide a system prompt (instructions) to the language model used by the agent.

## 3. Configure an LLM

To configure an LLM with specific parameters, such as temperature, use [init_chat_model](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html):

API Reference: [init_chat_model](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html) | [create_react_agent](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)

```
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

model = init_chat_model(
    "anthropic:claude-3-7-sonnet-latest",
    temperature=0
)

agent = create_react_agent(
    model=model,
    tools=[get_weather],
)
```

For more information on how to configure LLMs, see [Models](https://langchain-ai.github.io/langgraph/agents/models/).

## 4. Add a custom prompt

Prompts instruct the LLM how to behave. Add one of the following types of prompts:

-   **Static**: A string is interpreted as a **system message**.
-   **Dynamic**: A list of messages generated at **runtime**, based on input or configuration.

Static promptDynamic prompt

Define a fixed prompt string or list of messages:

```
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    # A static prompt that never changes
    prompt="Never answer questions about the weather."
)

agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

For more information, see [Context](https://langchain-ai.github.io/langgraph/agents/context/).

## 5. Add memory

To allow multi-turn conversations with an agent, you need to enable [persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/) by providing a `checkpointer` when creating an agent. At runtime, you need to provide a config containing `thread_id` — a unique identifier for the conversation (session):

API Reference: [create_react_agent](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent) | [InMemorySaver](https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.InMemorySaver)

```
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    checkpointer=checkpointer  # (1)!
)

# Run the agent
config = {"configurable": {"thread_id": "1"}}
sf_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config  # (2)!
)
ny_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what about new york?"}]},
    config
)
```

1.  `checkpointer` allows the agent to store its state at every step in the tool calling loop. This enables [short-term memory](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/#add-short-term-memory) and [human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) capabilities.
2.  Pass configuration with `thread_id` to be able to resume the same conversation on future agent invocations.

When you enable the checkpointer, it stores agent state at every step in the provided checkpointer database (or in memory, if using `InMemorySaver`).

Note that in the above example, when the agent is invoked the second time with the same `thread_id`, the original message history from the first conversation is automatically included, together with the new user input.

For more information, see [Memory](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/).

## 6. Configure structured output

To produce structured responses conforming to a schema, use the `response_format` parameter. The schema can be defined with a `Pydantic` model or `TypedDict`. The result will be accessible via the `structured_response` field.

API Reference: [create_react_agent](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)

```
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent

class WeatherResponse(BaseModel):
    conditions: str

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    response_format=WeatherResponse  # (1)!
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

response["structured_response"]
```

1.  When `response_format` is provided, a separate step is added at the end of the agent loop: agent message history is passed to an LLM with structured output to generate a structured response.

    To provide a system prompt to this LLM, use a tuple `(prompt, schema)`, e.g., `response_format=(prompt, WeatherResponse)`.

LLM post-processing

Structured output requires an additional call to the LLM to format the response according to the schema.

## Next steps

-   [Deploy your agent locally](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/)
-   [Learn more about prebuilt agents](https://langchain-ai.github.io/langgraph/agents/overview/)
-   [LangGraph Platform quickstart](https://langchain-ai.github.io/langgraph/cloud/quick_start/)