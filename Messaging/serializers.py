from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model  # Importar el modelo de usuario

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Message.
    Incluye un campo adicional 'sender_name' para representar el nombre de usuario del remitente.
    """
    sender_name = serializers.SerializerMethodField()  # Campo para el nombre del remitente

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'conversation', 'content', 'timestamp']

    def get_sender_name(self, obj):
        """
        Obtiene el nombre de usuario del remitente.

        Args:
            obj (Message): La instancia del mensaje.

        Returns:
            str: El nombre de usuario del remitente.
        """
        return obj.sender.username  # Retorna el username del remitente

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Conversation.
    Incluye el campo 'messages' que utiliza el MessageSerializer para representar los mensajes en la conversación.
    """
    messages = MessageSerializer(many=True, read_only=True)  # Usa el MessageSerializer actualizado

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']