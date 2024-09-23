# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from Messaging.models import *
from .models import Notification
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        for user in instance.thread.participants.exclude(id=instance.sender.id):
            Notification.objects.create(recipient=user, message=instance)
