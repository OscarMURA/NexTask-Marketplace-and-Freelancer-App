# Messaging/urls.py

from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('freelancer/', views.freelancer_chat, name='freelancer_chat'),
    path('freelancer/<int:conversation_id>/', views.freelancer_chat, name='freelancer_chat'),
    path('client/', views.client_chat, name='client_chat'),
    path('client/<int:conversation_id>/', views.client_chat, name='client_chat'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('api/conversation/<int:conversation_id>/', views.get_conversation_messages, name='get_conversation_messages'),
]
