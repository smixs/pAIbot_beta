import logging
from openai import OpenAI
from config import OPENAI_API_KEY
from typing import List, Dict

logger = logging.getLogger(__name__)

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    logger.error("OpenAI API key is not set. OpenAI services will not be available.")
    client = None

def chat_completion(conversation_history: List[Dict[str, str]], model: str) -> str:
    """Send a chat completion request to OpenAI."""
    if not client:
        return "OpenAI services are not available due to missing API key."
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=conversation_history
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        return f"Error in chat completion: {str(e)}"

def transcribe_audio(audio_file: bytes) -> str:
    """Transcribe audio using OpenAI Whisper."""
    if not client:
        logger.error("OpenAI client is not initialized. Cannot transcribe audio.")
        return "OpenAI services are not available due to missing API key."
    try:
        logger.info(f"Attempting to transcribe audio file of size: {len(audio_file)} bytes")
        
        # Convert bytes to file-like object
        import io
        audio_file_obj = io.BytesIO(audio_file)
        audio_file_obj.name = 'voice_message.ogg'  # Set a filename with appropriate extension
        
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file_obj
        )
        logger.info("Audio transcription successful")
        return transcript.text
    except Exception as e:
        logger.error(f"Error in audio transcription: {str(e)}")
        return f"Error in audio transcription: {str(e)}"

def generate_image(prompt: str) -> str:
    """Generate an image using DALL-E 3."""
    if not client:
        return "OpenAI services are not available due to missing API key."
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        logger.error(f"Error in image generation: {str(e)}")
        return f"Error in image generation: {str(e)}"

def analyze_image(image_file: bytes) -> str:
    """Analyze an image using OpenAI's Vision capabilities."""
    if not client:
        return "OpenAI services are not available due to missing API key."
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_file.decode('utf-8')}"}}
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        return f"Error in image analysis: {str(e)}"
