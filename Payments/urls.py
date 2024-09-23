from django.urls import path
from . import views

urlpatterns = [
    path('create-payment/<int:project_id>/', views.create_payment, name='create_payment'),
    path('client/payments/', views.client_payment_history, name='client_payment_history'),
    path('freelancer/payments/', views.freelancer_payment_history, name='freelancer_payment_history'),
]
