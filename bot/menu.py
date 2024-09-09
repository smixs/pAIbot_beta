from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import MODELS
from bot.utils import set_user_model

async def show_model_selection_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the model selection menu."""
    keyboard = [
        [InlineKeyboardButton(model, callback_data=f"model:{model}")]
        for model in MODELS.keys()
    ]
    keyboard.append([InlineKeyboardButton("Image Generation (DALL-E 3)", callback_data="mode:image_gen")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select a model or mode:", reply_markup=reply_markup)

async def handle_model_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the model selection."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("model:"):
        model = query.data.split(":")[1]
        set_user_model(update.effective_user.id, model)
        await query.edit_message_text(f"Selected model: {model}")
    elif query.data == "mode:image_gen":
        await query.edit_message_text("You're now in image generation mode. Please provide a description for the image you want to generate.")
        context.user_data["mode"] = "image_gen"
