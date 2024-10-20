import pytest
from django import forms
from Comments.forms import CommentForm
from Comments.models import Comment

@pytest.mark.django_db
class TestCommentForm:
    
    def test_form_is_valid_with_valid_data(self):
        # Datos de prueba válidos
        data = {
            'content': 'Este es un comentario de prueba.'
        }
        form = CommentForm(data=data)
        assert form.is_valid()  # Verifica que el formulario es válido

    def test_form_is_invalid_without_content(self):
        # Datos de prueba inválidos (sin contenido)
        data = {
            'content': ''
        }
        form = CommentForm(data=data)
        assert not form.is_valid()  # Verifica que el formulario no es válido
        assert 'content' in form.errors  # Asegúrate de que hay errores en el campo 'content'
