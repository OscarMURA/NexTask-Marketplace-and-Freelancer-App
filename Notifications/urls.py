from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/create/', views.create_notification, name='create_notification'),
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]