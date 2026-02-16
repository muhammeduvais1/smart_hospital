from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_index, name='chatbot_index'),
    path('send_message/', views.send_message, name='send_message'),
    path('sessions/', views.chatbot_sessions, name='chatbot_sessions'),
    path('sessions/new/', views.create_session, name='create_session'),
    path('sessions/<int:session_id>/', views.chatbot_detail, name='chatbot_detail'),
    path('sessions/<int:session_id>/delete/', views.delete_session, name='delete_session'),
]
