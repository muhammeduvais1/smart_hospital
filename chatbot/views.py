import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ChatSession, ChatMessage
from .forms import ChatMessageForm
from .services import ChatBotService

logger = logging.getLogger(__name__)


@login_required
def chatbot_index(request):
    """Display chatbot interface"""
    # Get or create a default chat session for the user
    session, created = ChatSession.objects.get_or_create(
        user=request.user,
        title='Hospital Assistant'
    )
    
    messages = session.messages.all()
    form = ChatMessageForm()
    
    context = {
        'session': session,
        'messages': messages,
        'form': form,
    }
    
    return render(request, 'chatbot/index.html', context)


@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Handle chat message via AJAX"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        # Get the chat session
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        
        # Validate input
        chatbot = ChatBotService()
        is_valid, error_msg = chatbot.validate_input(user_message)
        
        if not is_valid:
            return JsonResponse({'error': error_msg}, status=400)
        
        # Save user message
        user_msg = ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_message
        )
        
        # Get response from Gemini API
        messages = chatbot.format_messages_for_api(session)
        
        assistant_response = chatbot.get_response(messages)
        
        # Save assistant message
        assistant_msg = ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=assistant_response
        )
        
        # Update session title if it's the first message
        if session.messages.count() <= 2:
            title = user_message[:50]
            session.title = title
            session.save()
        
        return JsonResponse({
            'success': True,
            'user_message': {
                'id': user_msg.id,
                'role': user_msg.role,
                'content': user_msg.content,
            },
            'assistant_message': {
                'id': assistant_msg.id,
                'role': assistant_msg.role,
                'content': assistant_msg.content,
            }
        })
    
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)


@login_required
def chatbot_sessions(request):
    """Display list of all chat sessions for the user"""
    sessions = ChatSession.objects.filter(user=request.user)
    
    context = {
        'sessions': sessions,
    }
    
    return render(request, 'chatbot/sessions.html', context)


@login_required
def create_session(request):
    """Create a new chat session"""
    session = ChatSession.objects.create(
        user=request.user,
        title='New Chat'
    )
    return redirect('chatbot_detail', session_id=session.id)


@login_required
def chatbot_detail(request, session_id):
    """Display specific chat session"""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages = session.messages.all()
    form = ChatMessageForm()
    
    context = {
        'session': session,
        'messages': messages,
        'form': form,
    }
    
    return render(request, 'chatbot/detail.html', context)


@login_required
def delete_session(request, session_id):
    """Delete a chat session"""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    
    if request.method == 'POST':
        session.delete()
        return redirect('chatbot_sessions')
    
    context = {'session': session}
    return render(request, 'chatbot/delete_confirm.html', context)
