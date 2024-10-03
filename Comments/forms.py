# Comments/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    Formulario para crear un nuevo comentario.
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...', 'class':'form-control form-textarea shadow-none'}),
        label='',
        help_text=''
    )

    class Meta:
        model = Comment
        fields = ['content']
