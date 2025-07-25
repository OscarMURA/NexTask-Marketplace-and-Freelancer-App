from django.urls import path
from . import views


urlpatterns = [
    path('freelancer/', views.freelancer_chat, name='freelancer_chat'),
    path('freelancer/<int:conversation_id>/', views.freelancer_chat, name='freelancer_chat'),
    path('client/', views.client_chat, name='client_chat'),
    path('client/<int:conversation_id>/', views.client_chat, name='client_chat'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('api/conversation/<int:conversation_id>/send/', views.send_message, name='send_message'),  # Nueva ruta para enviar mensajes
    path('api/conversation/<int:conversation_id>/', views.get_conversation_messages, name='get_conversation_messages'),
    path('get-messages/<int:conversation_id>/', views.get_messages, name='get_messages'),
    path('search-users/', views.search_users, name='search_users'),  # Ruta nueva para la búsqueda de usuarios
    path('api/check-conversation/<int:user_id>/', views.check_conversation, name='check_conversation'),

]