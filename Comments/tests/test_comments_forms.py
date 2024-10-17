# Comments/tests/test_comments_forms.py

import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from Projects.models import Task
from django.utils import timezone
from Comments.forms import CommentForm
from Comments.models import Comment
from Users.models import ClientProfile  # Asegúrate de importar ClientProfile


class CommentFormTest(TestCase):
    def setUp(self):
        """
        Configura un usuario y una tarea para ser utilizados en las pruebas del formulario.
        """
        User = get_user_model()
        self.user = User.objects.create_user(
            username='formuser',
            email='formuser@example.com',
            password='formpass123'
        )
        # Crear una instancia de ClientProfile para asociar con Task
        self.client_profile = ClientProfile.objects.create(
            user=self.user,
            company_name='Test Company',
            company_website='https://testcompany.com',
            country='US',
            city='Test City',
            phone='1234567890',
            address='123 Test Street'
            # Añade otros campos requeridos según tu modelo
        )
        # Crear una descripción válida para QuillField
        description_json = json.dumps({
            "delta": {
                "ops": [
                    { "insert": "This task is for form testing.\n" }
                ]
            },
            "html": "<p>This task is for form testing.</p>"
        })
        self.task = Task.objects.create(
            title='Form Test Task',
            description=description_json,
            start_date='2024-01-01',
            due_date='2024-02-01',
            budget=1000.00,
            client=self.client_profile
        )
    
    def test_comment_form_valid_data(self):
        """
        Prueba que el formulario es válido cuando se proporciona datos válidos.
        """
        form_data = {
            'content': 'This is a valid comment.'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.task = self.task
        comment.author = self.user
        comment.save()
        self.assertEqual(comment.content, 'This is a valid comment.')
        self.assertEqual(comment.task, self.task)
        self.assertEqual(comment.author, self.user)
    
    def test_comment_form_empty_content(self):
        """
        Prueba que el formulario es inválido cuando el contenido está vacío.
        """
        form_data = {
            'content': ''
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])
    
    def test_comment_form_content_too_long(self):
        """
        (Opcional) Prueba que el formulario maneja contenido excesivamente largo.
        """
        long_content = 'a' * 5000  # Ajusta la longitud según las restricciones del modelo
        form_data = {
            'content': long_content
        }
        form = CommentForm(data=form_data)
        # Asumiendo que no hay max_length establecido, ajusta en consecuencia
        self.assertTrue(form.is_valid())
        # Si hay un max_length, descomenta las siguientes líneas
        # self.assertFalse(form.is_valid())
        # self.assertIn('content', form.errors)
