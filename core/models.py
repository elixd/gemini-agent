import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import yaml

# Load environment variables, overriding any existing ones
load_dotenv(override=True)

# Load configuration from config.yaml
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)

def get_model():
    """
    Initializes and returns a ChatOpenAI model configured for OpenRouter.
    Settings are loaded from config.yaml.
    """
    model_settings = config['model_settings']
    model_name = model_settings['model_name']
    api_key_env_var = model_settings['api_key_env_var']
    base_url = model_settings['base_url']
    llm_parameters = model_settings.get('llm_parameters')
    if llm_parameters is None:
        llm_parameters = {}
    openrouter_reasoning_config = model_settings.get('openrouter_reasoning_config', {})

    api_key = os.getenv(api_key_env_var)
    if not api_key:
        raise ValueError(f"{api_key_env_var} environment variable not set.")

    extra_body = {}
    if openrouter_reasoning_config:
        extra_body["reasoning"] = openrouter_reasoning_config

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        extra_body=extra_body,
        **llm_parameters,
    )
