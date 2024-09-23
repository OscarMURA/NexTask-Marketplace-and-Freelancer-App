from django.urls import path
from . import views

urlpatterns = [
    path('freelancer/', views.freelancer_report, name='freelancer_report'),
    path('client/', views.client_report, name='client_report'),
]
