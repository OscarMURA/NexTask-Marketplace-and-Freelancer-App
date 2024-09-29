# Messaging/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.db.models import Q  # Importar Q para facilitar la búsqueda avanzada
from .forms import MessageForm

@login_required
def freelancer_chat(request, conversation_id=None):
    # Obtener las conversaciones del freelancer
    query = request.GET.get('search')
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Aplicar lógica de búsqueda si existe un término de búsqueda
    if query:
        conversations = conversations.filter(
            Q(participants__username__icontains=query) | Q(participants__first_name__icontains=query) | Q(participants__last_name__icontains=query)
        ).distinct()
    
    conversation = None
    messages = None

    if conversation_id:
        # Obtener la conversación seleccionada
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = conversation.messages.all()

        # Procesar el formulario de envío de mensaje
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.conversation = conversation
                message.sender = request.user
                message.save()
                return redirect('messaging:freelancer_chat', conversation_id=conversation.id)
    else:
        form = MessageForm()

    context = {
        'conversations': conversations,
        'conversation': conversation,
        'messages': messages,
        'form': form,
    }
    return render(request, 'messaging/freelancer_chat.html', context)

@login_required
def client_chat(request, conversation_id=None):
    # Obtener las conversaciones del cliente
    query = request.GET.get('search')
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Aplicar lógica de búsqueda si existe un término de búsqueda
    if query:
        conversations = conversations.filter(
            Q(participants__username__icontains=query) | Q(participants__first_name__icontains=query) | Q(participants__last_name__icontains=query)
        ).distinct()

    conversation = None
    messages = None

    if conversation_id:
        # Obtener la conversación seleccionada
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = conversation.messages.all()

        # Procesar el formulario de envío de mensaje
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.conversation = conversation
                message.sender = request.user
                message.save()
                return redirect('messaging:client_chat', conversation_id=conversation.id)
    else:
        form = MessageForm()

    context = {
        'conversations': conversations,
        'conversation': conversation,
        'messages': messages,
        'form': form,
    }
    return render(request, 'messaging/client_chat.html', context)
