from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model  # Importar el modelo de usuario

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # Campo para el nombre del remitente

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'conversation', 'content', 'timestamp']

    def get_sender_name(self, obj):
        return obj.sender.username  # Retorna el username del remitente

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Usa el MessageSerializer actualizado

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']
