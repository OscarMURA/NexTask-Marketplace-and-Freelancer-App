from django.urls import path
from . import views
from .views import freelancer_report, client_report

urlpatterns = [
    path('freelancer/', views.freelancer_report, name='freelancer_report'),  # URL para el informe del freelancer
    path('client/', views.client_report, name='client_report'),  # URL para el informe del cliente
]
