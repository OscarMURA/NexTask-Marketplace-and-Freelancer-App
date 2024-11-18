from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    """
    Formulario basado en el modelo Notification para crear y enviar notificaciones.

    Fields:
        recipient (ForeignKey): El usuario destinatario de la notificación.
        message (CharField): El contenido del mensaje de la notificación.
    """
    class Meta:
        model = Notification
        fields = ['recipient', 'message']

