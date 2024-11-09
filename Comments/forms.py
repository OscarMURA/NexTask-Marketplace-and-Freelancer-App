# Comments/forms.py

from django import forms
from .models import Comment, FreelancerComment
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

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

class FreelancerCommentForm(forms.ModelForm):
    """
    Formulario para crear un nuevo comentario con calificación para un freelancer.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    # Mantenemos el campo rating pero lo ocultamos en el formulario
    rating = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
        initial=0
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...', 'class':'form-control form-textarea shadow-none'}),
        label='Comentario'
    )
    
    class Meta:
        model = FreelancerComment
        fields = ['username', 'email', 'rating', 'comment']
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        rating = cleaned_data.get('rating')
        
        if not rating or not (1 <= rating <= 5):
            raise ValidationError("Por favor, selecciona una calificación de 1 a 5 estrellas.")
        
        if username and email:
            try:
                user = User.objects.get(username=username)
                if user.email != email:
                    raise ValidationError("El email no coincide con el username proporcionado.")
            except User.DoesNotExist:
                raise ValidationError("El username proporcionado no existe.")
        
        return cleaned_data