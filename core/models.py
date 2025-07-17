import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables, overriding any existing ones
load_dotenv(override=True)

def get_model(model_name="google/gemini-2.5-flash"):
    """
    Initializes and returns a ChatOpenAI model configured for OpenRouter.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set.")

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )
