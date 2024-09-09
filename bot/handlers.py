import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.menu import show_model_selection_menu
from bot.utils import get_user_model, set_user_model
from services.openai_service import chat_completion, transcribe_audio, generate_image, analyze_image
from services.anthropic_service import chat_with_claude
from config import MODELS, DEFAULT_MODEL
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

conversation_history = defaultdict(lambda: deque(maxlen=100))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Welcome to the AI Assistant Bot! You can interact with various AI models, transcribe audio, and generate images. Use /model to select a model or mode.')
    await show_model_selection_menu(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/model - Select an AI model\n"
        "You can also send text messages, audio messages, or images for processing."
    )
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user_id = update.effective_user.id
    model = get_user_model(user_id)
    
    # Add user message to conversation history
    conversation_history[user_id].append({"role": "user", "content": update.message.text})
    
    if MODELS[model] == "openai":
        response = chat_completion(list(conversation_history[user_id]), model)
    elif MODELS[model] == "anthropic":
        response = chat_with_claude(list(conversation_history[user_id]), model)
    else:
        response = "Unsupported model selected."
    
    # Add model response to conversation history
    conversation_history[user_id].append({"role": "assistant", "content": response})
    
    await update.message.reply_text(response)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming audio messages."""
    try:
        file = await update.message.voice.get_file()
        audio_file = await file.download_as_bytearray()
        
        logger.info(f"Received audio file of size: {len(audio_file)} bytes")
        
        transcription = transcribe_audio(audio_file)
        await update.message.reply_text(f"Transcription: {transcription}")
        
        # Add transcription to conversation history
        user_id = update.effective_user.id
        conversation_history[user_id].append({"role": "user", "content": transcription})
        
        # Process the transcription with the selected model
        model = get_user_model(user_id)
        if MODELS[model] == "openai":
            response = chat_completion(list(conversation_history[user_id]), model)
        elif MODELS[model] == "anthropic":
            response = chat_with_claude(list(conversation_history[user_id]), model)
        else:
            response = "Unsupported model selected."
        
        # Add model response to conversation history
        conversation_history[user_id].append({"role": "assistant", "content": response})
        
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in handle_audio: {str(e)}")
        await update.message.reply_text("Sorry, there was an error processing your audio message.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming images."""
    file = await update.message.photo[-1].get_file()
    image_file = await file.download_as_bytearray()
    
    description = analyze_image(image_file)
    await update.message.reply_text(f"Image description: {description}")
    
    # Ask if the user wants to generate an image
    await update.message.reply_text("Would you like me to generate an image based on this description? (Yes/No)")
    context.user_data["awaiting_image_generation"] = True
    context.user_data["image_description"] = description
