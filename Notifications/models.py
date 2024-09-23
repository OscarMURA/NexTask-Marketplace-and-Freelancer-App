from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    """
    Represents a notification for a user.

    Attributes:
        recipient (ForeignKey): The user who receives the notification.
        message (ForeignKey): The message associated with the notification.
        created_at (DateTimeField): The date and time when the notification was created.
        is_read (BooleanField): Indicates whether the notification has been read by the recipient.
    """
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    """
    The user who receives the notification.
    The on_delete=models.CASCADE option ensures that if the user is deleted,
    all associated notifications will also be deleted.
    """
    
    message = models.ForeignKey('Messaging.Message', on_delete=models.CASCADE)
    """
    The message associated with the notification.
    This establishes a relationship with the Message model from the Messaging app.
    The on_delete=models.CASCADE option ensures that if the message is deleted,
    the notification will also be deleted.
    """
    
    created_at = models.DateTimeField(default=timezone.now)
    """
    The date and time when the notification was created.
    Defaults to the current date and time when the notification is instantiated.
    """
    
    is_read = models.BooleanField(default=False)
    """
    Indicates whether the notification has been read by the recipient.
    Defaults to False, meaning the notification is unread.
    """

