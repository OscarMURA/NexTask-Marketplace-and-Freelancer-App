from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'Notifications'  # Esto está bien si el nombre de tu carpeta comienza con mayúscula
    
    def ready(self):
        import Notifications.signals  # Correcto, ya que el nombre de la app tiene mayúscula