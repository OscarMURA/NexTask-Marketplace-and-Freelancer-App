from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('notifications/', views.notification_list, name='notification_list'),  
    path('notifications/create/', views.create_notification, name='create_notification'),
    path('notifications/', views.notification_list, name='notification_list'), 
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('freelancer/', views.notification_list_freelancer, name='notifications_list_freelancer'),
    path('client/', views.notification_list_client, name='notifications_list_client'),
]

