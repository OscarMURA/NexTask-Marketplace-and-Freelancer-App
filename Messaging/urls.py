# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('start-thread/<int:user_id>/', views.start_thread, name='start_thread'),
]
