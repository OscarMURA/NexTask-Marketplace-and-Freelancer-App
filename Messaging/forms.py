# messaging/forms.py
from django import forms
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageForm(forms.ModelForm):
    """
    Formulario basado en el modelo Message para crear y enviar mensajes.
    
    Fields:
        content (CharField): Campo de texto para el contenido del mensaje, con un placeholder personalizado.
    """
    class Meta:
        model = Message
        fields = ('content',)  # Cambiar 'body' por 'content' para que coincida con el modelo actualizado
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Escribe un mensaje...'}),
        }

class UserSearchForm(forms.Form):
    """
    Formulario para buscar usuarios por nombre de usuario.
    
    Fields:
        username (CharField): Campo de texto para ingresar el nombre de usuario a buscar, con un placeholder personalizado.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Buscar usuario...'})
    )
