# messaging/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/messaging/<int:conversation_id>/', consumers.ChatConsumer.as_asgi()),
]