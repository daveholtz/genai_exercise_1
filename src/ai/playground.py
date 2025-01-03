from openai import OpenAI
from typing import Dict, Any
from ..config import OPENAI_API_KEY, DEFAULT_AI_PARAMS, LEGACY_MODEL, ADVANCED_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def get_model_name(assistance_level: str) -> str:
    """Get the appropriate model name based on assistance level."""
    return LEGACY_MODEL if assistance_level == "Legacy AI Model" else ADVANCED_MODEL


def get_ai_response(prompt: str, assistance_level: str) -> tuple[str, Dict[Any, Any]]:
    """
    Get AI response for a given prompt.
    Returns a tuple of (response: str, parameters: Dict[Any, Any])
    """
    model = get_model_name(assistance_level)
    parameters = {"model": model, **DEFAULT_AI_PARAMS}

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], **parameters
        )
        return response.choices[0].message.content, parameters
    except Exception as e:
        raise Exception(f"Error getting AI response: {str(e)}")
