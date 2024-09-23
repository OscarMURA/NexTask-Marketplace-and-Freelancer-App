from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey('Messaging.Message', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

