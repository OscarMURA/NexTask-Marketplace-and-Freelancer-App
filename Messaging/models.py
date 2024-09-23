from django.db import models

# Create your models here.
# messaging/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Thread(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Thread between {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
