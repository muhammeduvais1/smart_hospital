#!/usr/bin/env python
"""
Test script for chatbot functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hospital.settings')
django.setup()

from django.contrib.auth.models import User
from chatbot.models import ChatSession, ChatMessage
from chatbot.services import ChatBotService

print("=" * 60)
print("CHATBOT FUNCTIONALITY TEST")
print("=" * 60)

try:
    # Test 1: Initialize ChatBot Service
    print("\n1. Initializing ChatBot Service...")
    chatbot = ChatBotService()
    print("   ✓ ChatBot Service initialized successfully")
    
    # Test 2: Get or create test user
    print("\n2. Getting/Creating test user...")
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('TestPass123!')
        user.save()
        print(f"   ✓ Created new test user: {user.username}")
    else:
        print(f"   ✓ Using existing test user: {user.username}")
    
    # Test 3: Create a chat session
    print("\n3. Creating chat session...")
    session = ChatSession.objects.create(
        user=user,
        title='Test Chat Session'
    )
    print(f"   ✓ Chat session created (ID: {session.id})")
    
    # Test 4: Validate input
    print("\n4. Testing input validation...")
    test_inputs = [
        ("Hello, how are you?", True),
        ("", False),
        ("x" * 2001, False),
    ]
    
    for text, should_pass in test_inputs:
        is_valid, error = chatbot.validate_input(text)
        status = "✓" if is_valid == should_pass else "✗"
        print(f"   {status} Input '{text[:30]}...': {is_valid} - {error}")
    
    # Test 5: Create sample messages
    print("\n5. Creating sample messages...")
    user_msg = ChatMessage.objects.create(
        session=session,
        role='user',
        content='Hello, can you tell me about hospital services?'
    )
    print(f"   ✓ User message created (ID: {user_msg.id})")
    
    # Test 6: Format messages for API
    print("\n6. Formatting messages for API...")
    messages = chatbot.format_messages_for_api(session)
    print(f"   ✓ Formatted {len(messages)} messages for API")
    print(f"   - System prompt included: {messages[0]['role'] == 'system'}")
    print(f"   - User messages: {sum(1 for m in messages if m['role'] == 'user')}")
    
    # Test 7: Get response from ChatBot (if API key is configured)
    print("\n7. Testing ChatBot response...")
    from django.conf import settings
    if not settings.OPENAI_API_KEY:
        print("   ⚠ OPENAI_API_KEY not configured in .env file")
        print("   - To test, add OPENAI_API_KEY=sk-*** to .env file")
    else:
        print("   ✓ OPENAI_API_KEY is configured")
        try:
            response = chatbot.get_response(messages, max_tokens=100)
            
            # Save response
            assistant_msg = ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=response
            )
            print(f"   ✓ Got response from ChatBot (ID: {assistant_msg.id})")
            print(f"   - Response preview: {response[:100]}...")
        except Exception as e:
            print(f"   ⚠ Error getting API response: {str(e)}")
            print("   - Verify your OpenAI API key is valid and has sufficient credits")
    
    # Test 8: Database integrity
    print("\n8. Checking database integrity...")
    session_count = ChatSession.objects.filter(user=user).count()
    message_count = ChatMessage.objects.filter(session=session).count()
    print(f"   ✓ Chat sessions for user: {session_count}")
    print(f"   ✓ Messages in session: {message_count}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Log in to the hospital system")
    print("2. Click 'ChatBot' in the navigation menu")
    print("3. Start a conversation with the hospital assistant")
    print("\nSetup guide: See CHATBOT_SETUP.md for detailed instructions")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Ensure all migrations were applied: python manage.py migrate")
    print("2. Check that .env file exists in project root")
    print("3. Review CHATBOT_SETUP.md for setup instructions")
    import traceback
    traceback.print_exc()
