# Comments/tests/test_comments_models.py

import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from Projects.models import Task
from django.utils import timezone
from Comments.models import Comment
from Users.models import ClientProfile  # Asegúrate de importar ClientProfile


class CommentModelTest(TestCase):
    def setUp(self):
        """
        Configura un usuario y una tarea para ser utilizados en las pruebas del modelo.
        """
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
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
                    { "insert": "This is a test task.\n" }
                ]
            },
            "html": "<p>This is a test task.</p>"
        })
        self.task = Task.objects.create(
            title='Test Task',
            description=description_json,
            due_date='2024-02-01'  # Mantén solo los campos que existen en tu modelo
        )

    
    def test_create_comment(self):
        """
        Prueba que una instancia de Comment puede ser creada exitosamente.
        """
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content='This is a test comment.',
            created_at=timezone.now()
        )
        self.assertEqual(comment.task, self.task)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertIsNotNone(comment.created_at)
    
    def test_comment_str(self):
        """
        Prueba la representación en cadena (__str__) de una instancia de Comment.
        """
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content='Another test comment.',
            created_at=timezone.now()
        )
        expected_str = f'Comentario de {self.user.username} en {self.task.title}'
        self.assertEqual(str(comment), expected_str)
