import logging
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)


class ChatBotService:
    """Service class for handling OpenAI API interactions"""

    def __init__(self):
        """Initialize OpenAI client with API key from settings"""
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.model = settings.OPENAI_MODEL

    def get_response(self, messages, max_tokens=500):
        """
        Get response from OpenAI API

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens in response (default 500)

        Returns:
            str: The assistant's response or error message
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
                stop=None
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return f"I encountered an error processing your request. Please try again later."

    def format_messages_for_api(self, chat_session):
        """
        Format chat messages from session for OpenAI API

        Args:
            chat_session: ChatSession instance

        Returns:
            list: Formatted messages for API call
        """
        messages = []
        
        # Add system prompt for hospital assistant
        system_message = {
            "role": "system",
            "content": """You are a helpful medical assistant for a smart hospital system. 
You provide information about hospital services, appointment scheduling, medical records, 
and general health-related questions. Always maintain professionalism and encourage users 
to consult with doctors for serious medical concerns. If asked about emergency situations, 
advise the user to contact emergency services immediately."""
        }
        messages.append(system_message)
        
        # Add all previous messages from the session
        for message in chat_session.messages.all():
            messages.append({
                "role": message.role,
                "content": message.content
            })
        
        return messages

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
