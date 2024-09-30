from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from .forms import MessageForm
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q

User = get_user_model()

@login_required
def client_chat(request, conversation_id=None):
    # Fetch all users except the current user for initiating a new conversation
    users = User.objects.exclude(id=request.user.id)
    conversations = Conversation.objects.filter(participants=request.user)

    conversation = None
    messages = None
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = conversation.messages.all()

    form = MessageForm()

    if request.method == 'POST' and conversation:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('messaging:client_chat', conversation_id=conversation_id)

    context = {
        'users': users,
        'conversations': conversations,
        'conversation': conversation,
        'messages': messages,
        'form': form,
    }
    return render(request, 'messaging/client_chat.html', context)

@login_required
def freelancer_chat(request, conversation_id=None):
    # Fetch all users except the current user for initiating a new conversation
    users = User.objects.exclude(id=request.user.id)
    conversations = Conversation.objects.filter(participants=request.user)

    conversation = None
    messages = None
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = conversation.messages.all()

    form = MessageForm()

    if request.method == 'POST' and conversation:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('messaging:freelancer_chat', conversation_id=conversation_id)

    context = {
        'users': users,
        'conversations': conversations,
        'conversation': conversation,
        'messages': messages,
        'form': form,
    }
    return render(request, 'messaging/freelancer_chat.html', context)

@login_required
def start_conversation(request, user_id):
    # Get the user with whom the conversation is to be initiated
    other_user = get_object_or_404(User, id=user_id)

    # Busca si ya existe una conversación entre los dos usuarios
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).distinct().first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect('messaging:client_chat', conversation_id=conversation.id)

def get_conversation_messages(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    messages = conversation.messages.all()
    return JsonResponse({
        'messages': [
            {'sender': message.sender.username, 'content': message.content}
            for message in messages
        ]
    })
