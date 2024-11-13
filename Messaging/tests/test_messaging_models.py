# Messaging/tests/test_messaging_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from Messaging.models import Message, Conversation
from Messaging.serializers import MessageSerializer, ConversationSerializer

User = get_user_model()

class MessageSerializerTest(TestCase):

    def setUp(self):
        # Configurar usuarios de prueba y conversación
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])
        # Configurar mensaje de prueba
        self.message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Test message'
        )

    def test_message_serializer(self):
        # Probar la serialización del mensaje
        serializer = MessageSerializer(instance=self.message)
        data = serializer.data
        self.assertEqual(data['content'], 'Test message')  # Verificar el contenido
        self.assertEqual(data['sender'], self.user1.id)  # Verificar el campo sender
        self.assertEqual(data['sender_name'], 'user1')   # Verificar el campo sender_name
        self.assertEqual(data['conversation'], self.conversation.id)  # Verificar el campo conversation

    def test_message_deserialization(self):
        # Probar la deserialización del mensaje
        data = {
            'conversation': self.conversation.id,
            'sender': self.user1.id,
            'content': 'New message content'
        }
        serializer = MessageSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # Debe ser válido
        message = serializer.save()
        self.assertEqual(message.content, 'New message content')  # Verificar el contenido
        self.assertEqual(message.sender, self.user1)  # Verificar el remitente

class ConversationSerializerTest(TestCase):

    def setUp(self):
        # Configurar usuarios de prueba y conversación
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])
        # Crear mensajes
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Hello'
        )
        self.message2 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            content='Hi there'
        )

    def test_conversation_serializer(self):
        # Probar la serialización de la conversación
        serializer = ConversationSerializer(instance=self.conversation)
        data = serializer.data
        self.assertEqual(len(data['participants']), 2)  # Verifica la cantidad de participantes
        self.assertEqual(len(data['messages']), 2)      # Verifica la cantidad de mensajes
        self.assertEqual(data['messages'][0]['content'], 'Hello')  # Verifica el contenido del primer mensaje
        self.assertEqual(data['messages'][1]['content'], 'Hi there')  # Verifica el contenido del segundo mensaje
        self.assertEqual(data['messages'][0]['sender_name'], 'user1')  # Verifica sender_name del primer mensaje
        self.assertEqual(data['messages'][1]['sender_name'], 'user2')  # Verifica sender_name del segundo mensaje
