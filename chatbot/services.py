import logging
from django.conf import settings
from google import genai

logger = logging.getLogger(__name__)


class ChatBotService:
    """Service class for handling Google Gemini API interactions"""

    def __init__(self):
        """Initialize Gemini client with API key from settings"""
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured in environment variables")
        self.client = genai.Client(api_key=api_key)
        self.model = settings.GEMINI_MODEL
        self.system_instruction = """You are a helpful medical assistant for a smart hospital system. 
You provide information about hospital services, appointment scheduling, medical records, 
and general health-related questions. Always maintain professionalism and encourage users 
to consult with doctors for serious medical concerns. If asked about emergency situations, 
advise the user to contact emergency services immediately."""

    def get_response(self, messages, max_tokens=500):
        """
        Get response from Gemini API

        Args:
            messages: List of Content objects
            max_tokens: Maximum tokens in response (default 500)

        Returns:
            str: The assistant's response or error message
        """
        try:
            config = genai.types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.7,
                max_output_tokens=max_tokens,
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=config,
            )
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return f"I encountered an error processing your request. Please try again later."

    def format_messages_for_api(self, chat_session):
        """
        Format chat messages from session for Gemini API

        Args:
            chat_session: ChatSession instance

        Returns:
            list: Formatted Content models for API call
        """
        contents = []
        
        # Add all previous messages from the session
        for message in chat_session.messages.all():
            # Map OpenAI 'assistant' to Gemini 'model' role
            role = 'model' if message.role == 'assistant' else 'user'
            contents.append(
                genai.types.Content(
                    role=role,
                    parts=[genai.types.Part.from_text(text=message.content)]
                )
            )
        
        return contents

    def validate_input(self, user_message):
        """
        Validate user input before sending to API

        Args:
            user_message: User's message string

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        if not user_message or not user_message.strip():
            return False, "Please enter a message."
        
        if len(user_message) > 2000:
            return False, "Message is too long. Please keep it under 2000 characters."
        
        return True, ""
