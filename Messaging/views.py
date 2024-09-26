from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Thread, Message
from .forms import MessageForm

@login_required
def thread_list(request):
    threads = Thread.objects.filter(participants=request.user)
    return render(request, 'messaging/thread_list.html', {'threads': threads})

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, participants=request.user)
    messages = thread.messages.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = MessageForm()
    return render(request, 'messaging/thread_detail.html', {'thread': thread, 'messages': messages, 'form': form})

@login_required
def start_thread(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    thread = Thread.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not thread:
        thread = Thread.objects.create()
        thread.participants.add(request.user, other_user)
    return redirect('thread_detail', thread_id=thread.id)
