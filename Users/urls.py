from django.urls import path
from . import views

urlpatterns = [
    path('signup/freelancer/', views.freelancer_signup, name='register_freelancer'),
    path('signup/client/', views.client_signup, name='client_signup'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
]
