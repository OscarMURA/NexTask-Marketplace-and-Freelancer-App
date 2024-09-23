from django.db import models

# messaging/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Thread(models.Model):
    """
    Represents a conversation thread between users.

    Attributes:
        participants (ManyToManyField): Users participating in the thread.
        created_at (DateTimeField): Timestamp when the thread was created.
    """
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Returns a string representation of the thread with participant usernames."""
        return f"Thread between {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    """
    Represents a message within a conversation thread.

    Attributes:
        thread (ForeignKey): The thread to which the message belongs.
        sender (ForeignKey): The user who sent the message.
        body (TextField): The content of the message.
        timestamp (DateTimeField): Timestamp when the message was sent.
    """
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Returns a string representation of the message with sender username and timestamp."""
        return f"Message from {self.sender.username} at {self.timestamp}"
