from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from .forms import NotificationForm

@login_required
def notification_list(request):
    """
    Displays a list of notifications for the logged-in user.

    This view retrieves all notifications associated with the currently authenticated user
    and renders them in the notification list template.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: Renders the notification list template with the user's notifications.
    """
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def create_notification(request):
    """
    Creates a new notification.

    This view handles both GET and POST requests. For GET requests, it displays a form to create a new notification.
    For POST requests, it processes the form data to create and save the notification.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: Redirects to the notification list on successful creation or renders the notification creation form.
    """
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notification_list')
    else:
        form = NotificationForm()
    return render(request, 'notifications/create_notification.html', {'form': form})

@login_required
def mark_as_read(request, notification_id):
    """
    Marks a notification as read.

    This view retrieves the specified notification by its ID and marks it as read for the current user.

    Args:
        request (HttpRequest): The incoming request.
        notification_id (int): The ID of the notification to mark as read.

    Returns:
        HttpResponse: Redirects to the notification list after updating the notification's status.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')
