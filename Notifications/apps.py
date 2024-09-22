from django.apps import AppConfig


# notifications/apps.py
from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        import notifications.signals  # Import the signals module
