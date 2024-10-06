# messaging/forms.py
from django import forms
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)  # Cambiar 'body' por 'content' para que coincida con el modelo actualizado
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Escribe un mensaje...'}),
        }

class UserSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Buscar usuario...'})
    )
