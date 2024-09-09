import logging
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY
from typing import List, Dict

logger = logging.getLogger(__name__)

if ANTHROPIC_API_KEY:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    logger.error("Anthropic API key is not set. Anthropic services will not be available.")
    client = None

def chat_with_claude(conversation_history: List[Dict[str, str]], model: str) -> str:
    """Send a chat request to Anthropic's Claude model."""
    if not client:
        return "Anthropic services are not available due to missing API key."
    try:
        message = client.messages.create(
            model=model,
            max_tokens=1000,
            messages=conversation_history
        )
        return message.content[0].text
    except Exception as e:
        logger.error(f"Error in Claude chat: {str(e)}")
        return f"Error in Claude chat: {str(e)}"
