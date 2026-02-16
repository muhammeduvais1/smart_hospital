# SmartHospital Chatbot Setup Guide

## Overview
The SmartHospital system now includes an AI-powered chatbot using OpenAI's GPT API. The chatbot helps users with hospital-related inquiries and maintains conversation history.

## Prerequisites

The following packages have been installed:
- `openai` - OpenAI Python SDK
- `python-dotenv` - Environment variable management

## Configuration

### 1. Set Up Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Create a new API key
3. Copy the API key
4. Open the `.env` file in the project root
5. Replace `your-openai-api-key-here` with your actual API key:

```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### 2. Verify Environment Configuration

The following settings are already configured in `smart_hospital/settings.py`:

```python
# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = 'gpt-3.5-turbo'
```

## Features

### ChatBot Capabilities
- **Conversation Management**: Users can start multiple chat sessions
- **Hospital Assistant**: Trained to help with hospital services, appointments, and health queries
- **Message History**: All conversations are stored in the database
- **Real-time Response**: AJAX-based chat interface for smooth interaction
- **Session Management**: Create, view, and delete chat sessions

### Frontend Interface
- **Main Chat View** (`/chatbot/`): Real-time chat interface
- **Sessions List** (`/chatbot/sessions/`): View all past conversations
- **Session Detail** (`/chatbot/sessions/<id>/`): Specific chat session view
- **Delete Session** (`/chatbot/sessions/<id>/delete/`): Remove a chat session

## Database Models

### ChatSession
- `user`: ForeignKey to User (automatically associates chat with logged-in user)
- `created_at`: Timestamp of session creation
- `updated_at`: Timestamp of last message
- `title`: Custom title for the conversation

### ChatMessage
- `session`: ForeignKey to ChatSession
- `role`: Either 'user' or 'assistant'
- `content`: The actual message text
- `created_at`: Timestamp of message

## Usage

### For Users
1. Log in to the hospital system
2. Click **ChatBot** in the navigation menu
3. Start typing your message
4. Click **Send** or press Enter
5. The chatbot will respond within seconds
6. Create new chat sessions to organize conversations
7. View all past sessions in the history

### For Developers

#### ChatBotService Class
Location: `chatbot/services.py`

```python
from chatbot.services import ChatBotService

# Initialize service
chatbot = ChatBotService()

# Format messages for API
messages = chatbot.format_messages_for_api(chat_session)

# Get response
response = chatbot.get_response(messages)

# Validate input
is_valid, error_msg = chatbot.validate_input(user_message)
```

## System Prompt

The chatbot is initialized with the following system prompt:

```
You are a helpful medical assistant for a smart hospital system. 
You provide information about hospital services, appointment scheduling, medical records, 
and general health-related questions. Always maintain professionalism and encourage users 
to consult with doctors for serious medical concerns. If asked about emergency situations, 
advise the user to contact emergency services immediately.
```

You can customize this prompt by editing the `format_messages_for_api()` method in `chatbot/services.py`.

## API Integration Details

### OpenAI API Call Parameters
- **Model**: `gpt-3.5-turbo` (can be changed in settings)
- **Max Tokens**: 500 (configurable per request)
- **Temperature**: 0.7 (for balanced responses)
- **Stop**: None (let model decide when to stop)

### Error Handling
- Invalid API key: Will raise `ValueError` on initialization
- API errors: Returns user-friendly error message
- Empty messages: Validated before sending to API
- Long messages: Limited to 2000 characters

## Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chatbot/` | GET | Main chat interface |
| `/chatbot/send_message/` | POST | Send message (AJAX) |
| `/chatbot/sessions/` | GET | List all sessions |
| `/chatbot/sessions/new/` | GET | Create new session |
| `/chatbot/sessions/<id>/` | GET | View specific session |
| `/chatbot/sessions/<id>/delete/` | POST | Delete session |

## Customization

### Modify System Prompt
Edit `chatbot/services.py`, method `format_messages_for_api()`:

```python
system_message = {
    "role": "system",
    "content": "Your custom system prompt here..."
}
```

### Change Model
Edit `smart_hospital/settings.py`:

```python
OPENAI_MODEL = 'gpt-4'  # or any other available model
```

### Adjust Response Length
In `chatbot/views.py`, modify the `send_message()` view:

```python
assistant_response = chatbot.get_response(messages, max_tokens=1000)
```

## Security Considerations

1. **API Key Protection**: 
   - Never commit `.env` file to version control
   - Add `.env` to `.gitignore`
   - Use different keys for development and production

2. **User Privacy**:
   - Chat history is stored directly in the database
   - Only authenticated users can access the chatbot
   - Users can only see their own chat sessions

3. **Input Validation**:
   - Messages are validated for length (max 2000 chars)
   - Empty messages are rejected
   - SQL injection is prevented by Django ORM

## Troubleshooting

### Issue: "OPENAI_API_KEY is not configured"
**Solution**: Ensure your `.env` file has the correct API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### Issue: "Invalid API Key"
**Solution**: Verify your OpenAI API key is correct and hasn't expired

### Issue: Messages not saving
**Solution**: Check that migrations were applied:
```bash
python manage.py migrate chatbot
```

### Issue: CSS/styling not loading
**Solution**: Ensure Bootstrap CDN is available and static files are configured

## Performance Notes

- **Response Time**: Typically 2-5 seconds depending on API latency
- **Database**: Uses SQLite (fine for development, consider PostgreSQL for production)
- **Scalability**: Consider implementing async tasks with Celery for very high traffic

## Future Enhancements

Potential improvements:
1. **Streaming Responses**: Real-time token streaming for faster perceived responses
2. **Conversation Export**: Download chat history as PDF/TXT
3. **Multi-language Support**: Translate conversations
4. **File Upload**: Allow users to upload medical documents for context
5. **Analytics**: Track common questions and user satisfaction
6. **Integration with Hospital Data**: Context-aware responses using patient records
7. **Voice Input/Output**: Speech-to-text and text-to-speech
8. **Admin Dashboard**: Monitor chatbot performance and user interactions

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review OpenAI documentation: https://platform.openai.com/docs
3. Check Django documentation: https://docs.djangoproject.com

---

**Last Updated**: February 16, 2026
**Chatbot Version**: 1.0
