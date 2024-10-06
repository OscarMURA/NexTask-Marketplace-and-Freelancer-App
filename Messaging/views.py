from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import generics
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

User = get_user_model()

@login_required
def client_chat(request, conversation_id=None):
    users = User.objects.exclude(id=request.user.id)
    conversations = Conversation.objects.filter(participants=request.user)

    conversation = None
    messages = []
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    context = {
        'users': users,
        'conversations': conversations,
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'messaging/client_chat.html', context)

@login_required
def freelancer_chat(request, conversation_id=None):
    current_user = request.user  # Usuario actual

    # Obtener todas las conversaciones activas del usuario actual
    conversations = Conversation.objects.filter(participants=current_user)

    # Inicializamos active_users como una consulta vacía para evitar el error UnboundLocalError
    active_users = User.objects.none()

    # Si hay conversaciones activas, obtenemos los usuarios que participan en ellas
    if conversations.exists():
        active_users = User.objects.filter(conversations__in=conversations).exclude(id=current_user.id).distinct()

    # Excluimos los usuarios con los que ya hay una conversación activa
    users = User.objects.exclude(id__in=active_users.values_list('id', flat=True)).exclude(id=current_user.id)

    conversation = None
    messages = []
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    context = {
        'users': users,  # Usuarios disponibles
        'conversations': conversations,  # Conversaciones activas
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'messaging/freelancer_chat.html', context)

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    # Busca si ya existe una conversación entre los dos usuarios
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect('messaging:client_chat', conversation_id=conversation.id)

# API para obtener y enviar mensajes
@api_view(['GET'])
def get_conversation_messages(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversación no encontrada o no tienes permiso para verla."}, status=404)

    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def send_message(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversación no encontrada o no tienes permiso para enviar mensajes."}, status=404)

    content = request.data.get('content')
    if not content or content.strip() == '':
        return Response({"error": "El contenido del mensaje no puede estar vacío."}, status=400)

    message_data = {
        'conversation': conversation.id,
        'sender': request.user.id,
        'content': content
    }

    serializer = MessageSerializer(data=message_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# API Views
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ConversationDetailView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer