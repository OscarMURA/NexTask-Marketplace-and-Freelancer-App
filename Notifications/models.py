from django.db import models

# Create your models here.
# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from messaging.models import Thread, Message

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - Message from {self.message.sender.username}"
