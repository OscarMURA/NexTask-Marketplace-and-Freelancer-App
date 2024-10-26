from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from Messaging.models import Conversation, Message

User = get_user_model()

class ChatViewTests(TestCase):

    def setUp(self):
        # Crear usuarios de prueba
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Crear una conversación entre los usuarios
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)

    def test_client_chat_view_authenticated(self):
        # Probar la vista de chat para el cliente estando autenticado
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('messaging:client_chat', args=[self.conversation.id]))
        self.assertEqual(response.status_code, 200)

    def test_freelancer_chat_view_authenticated(self):
        # Probar la vista de chat para el freelancer estando autenticado
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('messaging:freelancer_chat', args=[self.conversation.id]))
        self.assertEqual(response.status_code, 200)

    def test_start_conversation_creates_new(self):
        # Probar que se crea una nueva conversación al iniciar una conversación
        self.client.login(username='user1', password='password1')
        response = self.client.post(reverse('messaging:start_conversation', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)  # Redirección después de crear la conversación

    def test_check_conversation(self):
        # Probar la vista para verificar si existe una conversación con otro usuario
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('messaging:check_conversation', args=[self.user2.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_conversation_messages(self):
        # Probar la vista para obtener los mensajes de una conversación
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('messaging:get_conversation_messages', args=[self.conversation.id]))
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        # Probar la funcionalidad para enviar un mensaje en una conversación
        self.client.login(username='user1', password='password1')
        response = self.client.post(reverse('messaging:send_message', args=[self.conversation.id]), {'content': 'Hello'})
        self.assertEqual(response.status_code, 201)  # El mensaje debería crearse correctamente

    def test_search_users(self):
        # Probar la funcionalidad de búsqueda de usuarios
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('messaging:search_users') + '?q=user')
        self.assertEqual(response.status_code, 200)
