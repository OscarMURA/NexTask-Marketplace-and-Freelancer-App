from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notification
from Messaging.models import Message

@receiver(post_save, sender=Message)
def create_notification(sender, instance, **kwargs):
    # Using `conversation` instead of `thread`
    for user in instance.conversation.participants.exclude(id=instance.sender.id):
        Notification.objects.create(
            recipient=user,
            message=instance,  # Pasamos la instancia del mensaje en lugar de un string
            is_read=False
        )