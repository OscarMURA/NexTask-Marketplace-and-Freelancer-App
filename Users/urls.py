# Users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('signup/freelancer/', views.freelancer_signup, name='freelancer_signup'),
    path('signup/client/', views.client_signup, name='client_signup'),
]
