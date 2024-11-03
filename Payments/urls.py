from django.urls import path
from . import views

urlpatterns = [
    path('client/payments/', views.client_payment_history, name='client_payment_history'),
    path('freelancer/payments/', views.freelancer_payment_history, name='freelancer_payment_history'),
    path('freelancers_project_pay/<int:project_id>/', views.freelancers_project_pay, name='freelancers_project_pay'),
]
