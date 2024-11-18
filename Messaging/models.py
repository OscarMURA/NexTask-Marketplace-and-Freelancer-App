# messaging/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()

class Conversation(models.Model):
    """
    Modelo para representar una conversación entre usuarios.
    
    Attributes:
        participants (ManyToManyField): Los usuarios que participan en la conversación.
    """
    participants = models.ManyToManyField(User, related_name='conversations')

class Message(models.Model):
    """
    Modelo para representar un mensaje dentro de una conversación.
    
    Attributes:
        conversation (ForeignKey): La conversación a la que pertenece el mensaje.
        sender (ForeignKey): El usuario que envió el mensaje.
        content (TextField): El contenido del mensaje.
        timestamp (DateTimeField): La fecha y hora en que se creó el mensaje.
    """
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
        Retorna una representación en cadena del mensaje.

        Returns:
            str: Una cadena que muestra el remitente y el contenido del mensaje.
        """
        return f"Message from {self.sender.username}: {self.content}"