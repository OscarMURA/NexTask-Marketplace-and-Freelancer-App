from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from .forms import NotificationForm
from django.contrib import messages

@login_required
def notification_list(request):
    """
    Displays a list of notifications for the logged-in user based on their user type.
    """
    notifications = Notification.objects.filter(recipient=request.user)

    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        print(f"Intentando eliminar la notificación con ID: {notification_id}")
        try:
            notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
            notification.delete()  # Eliminar la notificación
            messages.success(request, "Notificación eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la notificación: {e}")
            messages.error(request, "No se pudo eliminar la notificación.")

        return redirect('notification_list')  # Redirigir a la misma vista de notificaciones

    # Utiliza el tipo de usuario para redirigir a la plantilla correcta
    if request.user.is_freelancer:
        return render(request, 'notifications_list_freelancer.html', {'notifications': notifications})
    elif request.user.is_client:
        return render(request, 'notifications_list_client.html', {'notifications': notifications})
    else:
        print("hola no debería pasar esto")
        messages.error(request, "No se pudo determinar el tipo de usuario.")
        return redirect('home')
    
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
def notification_list_freelancer(request):
    """
    Displays a list of notifications for the freelancer.
    """
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications_list_freelancer.html', {'notifications': notifications})

@login_required
def notification_list_client(request):
    """
    Displays a list of notifications for the client.
    """
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications_list_client.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    """
    Marks a notification as read and deletes it.

    This view retrieves the specified notification by its ID and deletes it for the current user.

    Args:
        request (HttpRequest): The incoming request.
        notification_id (int): The ID of the notification to mark as read and delete.

    Returns:
        HttpResponse: Redirects to the notification list after deleting the notification.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()  # Eliminar la notificación en lugar de solo marcarla
    return redirect('notification_list')