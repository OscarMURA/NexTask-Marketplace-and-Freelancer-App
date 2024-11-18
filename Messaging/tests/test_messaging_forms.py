# Messaging/tests/test_serializers.py
from django.test import TestCase
from Messaging.serializers import MessageSerializer, ConversationSerializer
from Messaging.models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializerTest(TestCase):
    def setUp(self):
        # Crear un usuario y un mensaje de ejemplo para las pruebas
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.conversation = Conversation.objects.create()  # Crear una conversación
        self.message = Message.objects.create(
            sender=self.user,
            conversation=self.conversation,
            content='Test message content',
        )
        self.message_data = {
            'sender': self.user.id,
            'conversation': self.conversation.id,
            'content': 'Serialized test message',
        }

    def test_message_serializer_valid_data(self):
        # Probar el serializador con datos válidos
        serializer = MessageSerializer(data=self.message_data)
        self.assertTrue(serializer.is_valid())

    def test_message_serializer_invalid_data(self):
        # Probar el serializador con campos requeridos faltantes
        invalid_data = {'content': 'Message without sender or conversation'}
        serializer = MessageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('sender', serializer.errors)
        self.assertIn('conversation', serializer.errors)

    def test_message_serializer_output(self):
        # Probar la salida del serializador con una instancia de mensaje existente
        serializer = MessageSerializer(instance=self.message)
        self.assertEqual(serializer.data['content'], 'Test message content')
        self.assertEqual(serializer.data['sender'], self.user.id)
        self.assertEqual(serializer.data['sender_name'], 'testuser')

class ConversationSerializerTest(TestCase):
    def setUp(self):
        # Crear usuarios y una conversación de ejemplo para las pruebas
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])
        self.message1 = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            content='First message content',
        )
        self.message2 = Message.objects.create(
            sender=self.user2,
            conversation=self.conversation,
            content='Second message content',
        )

    def test_conversation_serializer_valid_data(self):
        # Probar la serialización de la conversación con mensajes
        serializer = ConversationSerializer(instance=self.conversation)
        self.assertEqual(serializer.data['id'], self.conversation.id)
        self.assertEqual(len(serializer.data['messages']), 2)  # Verificar que todos los mensajes estén incluidos
        self.assertEqual(serializer.data['messages'][0]['content'], 'First message content')
        self.assertEqual(serializer.data['messages'][1]['content'], 'Second message content')

    def test_conversation_serializer_empty_messages(self):
        # Probar la salida del serializador cuando no hay mensajes en la conversación
        empty_conversation = Conversation.objects.create()
        serializer = ConversationSerializer(instance=empty_conversation)
        self.assertEqual(serializer.data['messages'], [])
