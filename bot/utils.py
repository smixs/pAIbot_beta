from typing import Dict
from config import DEFAULT_MODEL

user_models: Dict[int, str] = {}

def get_user_model(user_id: int) -> str:
    """Get the selected model for a user."""
    return user_models.get(user_id, DEFAULT_MODEL)

def set_user_model(user_id: int, model: str) -> None:
    """Set the selected model for a user."""
    user_models[user_id] = model
