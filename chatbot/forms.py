from django import forms
from .models import ChatMessage


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 3,
                'id': 'chat-input'
            })
        }
