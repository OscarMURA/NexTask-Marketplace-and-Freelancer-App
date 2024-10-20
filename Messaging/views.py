from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Thread, Message
from .forms import MessageForm
from django.utils.translation import gettext as _
from Notifications.models import Notification
from django.utils import timezone

@login_required
def thread_list(request):
    """
    Displays a list of conversation threads that the user participates in.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered template showing the user's threads.
    """
    threads = Thread.objects.filter(participants=request.user)
    return render(request, 'messaging/thread_list.html', {'threads': threads})

@login_required
def thread_detail(request, thread_id):
    """
    Displays the details of a specific conversation thread, including messages.

    Args:
        request: The HTTP request object.
        thread_id (int): The ID of the thread to display.

    Returns:
        Rendered template showing the thread details and messages.
    """
    thread = get_object_or_404(Thread, id=thread_id, participants=request.user)
    messages = thread.messages.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            
            recipient = thread.participants.exclude(id=request.user.id).first()  # Obtener el otro participante
            notification_message = _("You have a new message from %(username)s in the chat.") % {
                'username': request.user.username  # Asumiendo que 'username' es el campo que contiene el nombre del usuario
            }

            Notification.objects.create(
                recipient=recipient,  # El otro usuario que recibe la notificación
                message=notification_message,
                created_at=timezone.now()  # No es necesario si ya tienes el valor predeterminado en el modelo
            )

            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = MessageForm()
    return render(request, 'messaging/thread_detail.html', {'thread': thread, 'messages': messages, 'form': form})

@login_required
def start_thread(request, user_id):
    """
    Starts a new conversation thread with another user.

    Args:
        request: The HTTP request object.
        user_id (int): The ID of the user to start a thread with.

    Returns:
        Redirects to the thread detail view for the new or existing thread.
    """
    other_user = get_object_or_404(User, id=user_id)
    thread = Thread.objects.filter(participants=request.user).filter(participants=other_user).first()

        # Crear la notificación para el usuario con el que se inicia el chat
    notification_message = _("%(username)s is starting a new conversation with you") % {
        'username': request.user.username  # Asumiendo que 'username' es el campo que contiene el nombre del usuario
    }

    Notification.objects.create(
        recipient=other_user,  # El otro usuario que recibe la notificación
        message=notification_message,
        created_at=timezone.now()  # No es necesario si ya tienes el valor predeterminado en el modelo
    )

    if not thread:
        thread = Thread.objects.create()
        thread.participants.add(request.user, other_user)
    
    return redirect('thread_detail', thread_id=thread.id)
