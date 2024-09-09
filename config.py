import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN is not set in the environment variables.")

# OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in the environment variables.")

# Anthropic API Key
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    logger.error("ANTHROPIC_API_KEY is not set in the environment variables.")

# Available models
MODELS = {
    "claude-3-5-sonnet-20240620": "anthropic",
    "claude-3-opus-20240229": "anthropic",
    "chatgpt-4o-latest": "openai",
    "gpt-4o-mini": "openai",
}

# Default model
DEFAULT_MODEL = "chatgpt-4o-latest"

# Check if all required API keys are set
if not all([TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, ANTHROPIC_API_KEY]):
    logger.warning("One or more required API keys are missing. Some features may not work.")
