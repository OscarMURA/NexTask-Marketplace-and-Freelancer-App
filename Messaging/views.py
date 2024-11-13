from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from Notifications.models import Notification
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import generics
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.db.models import Count
from .models import User
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone

User = get_user_model()

@login_required
def client_chat(request, conversation_id=None):
    """
    Renders the client chat interface, loading all users, conversations, and messages for a specific conversation if provided.

    Args:
        request (HttpRequest): The incoming request object.
        conversation_id (int, optional): ID of a specific conversation to load. Defaults to None.

    Returns:
        HttpResponse: Renders the 'client_chat.html' template with context containing users, conversations, conversation, and messages.
    """
     
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
    """
    Renders the freelancer chat interface, loading all active conversations for the current user and available users for new conversations.

    Args:
        request (HttpRequest): The incoming request object.
        conversation_id (int, optional): ID of a specific conversation to load. Defaults to None.

    Returns:
        HttpResponse: Renders the 'freelancer_chat.html' template with context containing users, conversations, conversation, and messages.
    """
    current_user = request.user  # Usuario actual

    # Obtener todas las conversaciones activas del usuario actual
    conversations = Conversation.objects.filter(participants=current_user).annotate(num_messages=Count('messages')).filter(num_messages__gt=0)

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
    """
    Starts a new conversation with another user if it doesn't already exist, and sends a notification to that user.

    Args:
        request (HttpRequest): The incoming request object.
        user_id (int): ID of the user with whom to start a conversation.

    Returns:
        HttpResponseRedirect: Redirects to the client chat view with the new conversation's ID.
    """
    other_user = get_object_or_404(User, id=user_id)
    # Busca si ya existe una conversación entre los dos usuarios
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

        message = _("A new conversation has been started with %(username)s.") % {
            'username': other_user.username,
        }
        Notification.objects.create(
            recipient=other_user,
            message=message,
            created_at=timezone.now()
        )

    return redirect('messaging:client_chat', conversation_id=conversation.id)

# API para obtener y enviar mensajes
@api_view(['GET'])
def get_conversation_messages(request, conversation_id):
    """
    API view to retrieve messages from a specific conversation if the user is a participant.

    Args:
        request (HttpRequest): The incoming request object.
        conversation_id (int): ID of the conversation.

    Returns:
        Response: JSON response with serialized messages or error if the conversation is not found.
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversación no encontrada o no tienes permiso para verla."}, status=404)

    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def send_message(request, conversation_id):
    """
    API view to send a message in a specific conversation if the user is a participant.
    Sends a notification to the other participant.

    Args:
        request (HttpRequest): The incoming request object with message content.
        conversation_id (int): ID of the conversation.

    Returns:
        Response: JSON response with the new message or error if the content is empty or conversation is not found.
    """
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

        other_participant = conversation.participants.exclude(id=request.user.id).first()
        if other_participant:
            notification_message = _("You have received a new message from %(sender)s.") % {
                'sender': request.user.username
            }
            Notification.objects.create(
                recipient=other_participant,
                message=notification_message,
                created_at=timezone.now()
            )

        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# API Views
class MessageListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating messages in a conversation.
    Allows authenticated users to retrieve and send messages in a specific conversation.

    Attributes:
        serializer_class (Serializer): Serializer for Message model.
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ConversationDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific conversation.
    
    Attributes:
        queryset (QuerySet): Queryset for retrieving Conversation model instances.
        serializer_class (Serializer): Serializer for Conversation model.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
def get_messages(request, conversation_id):
    """
    API view to retrieve messages in a conversation as JSON, ordered by timestamp.

    Args:
        request (HttpRequest): The incoming request object.
        conversation_id (int): ID of the conversation.

    Returns:
        JsonResponse: JSON response with a list of serialized messages.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
        message_list = [{
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        } for message in messages]
        return JsonResponse({'messages': message_list})

@login_required
def search_users(request):
    """
    Searches for users by username starting with a query string (case insensitive).
    Excludes the current user from the results.

    Args:
        request (HttpRequest): The incoming request object containing a search query.

    Returns:
        JsonResponse: JSON response with a list of matching users or an empty list if no query is provided.
    """
    query = request.GET.get('q', '').strip()
    if query:
        # Filtrar los usuarios cuyo nombre de usuario comienza con la cadena ingresada (case insensitive)
        users = User.objects.filter(Q(username__istartswith=query)).exclude(id=request.user.id)[:10]
        users_data = [
            {
                'id': user.id,
                'username': user.username,
                'profile_picture': getattr(user, 'profile_picture', None).url if getattr(user, 'profile_picture', None) else (
                    f'{settings.STATIC_URL}img/defaultFreelancerProfileImage.jpg' if user.user_type == 'freelancer' else
                    f'{settings.STATIC_URL}img/defaultClientProfileImage.png'
                )
            }

            for user in users
        ]
        return JsonResponse({'users': users_data})
    return JsonResponse({'users': []})


def check_conversation(request, user_id):
    """
    Checks if a conversation exists between the current user and another specified user.

    Args:
        request (HttpRequest): The incoming request object.
        user_id (int): ID of the other user.

    Returns:
        JsonResponse: JSON response indicating if the conversation exists and its ID if so.
    """
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)

    # Verificar si ya existe una conversación entre los usuarios
    conversation = Conversation.objects.filter(participants=current_user).filter(participants=other_user).first()

    if conversation:
        return JsonResponse({'conversation_exists': True, 'conversation_id': conversation.id})
    else:
        return JsonResponse({'conversation_exists': False})