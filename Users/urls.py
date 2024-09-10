from django.urls import path
from . import views

urlpatterns = [
    path('signup/freelancer/', views.freelancer_signup, name='register_freelancer'),
    path('signup/client/', views.client_signup, name='client_signup'),
    path('education/register/', views.education_register_view, name='education_register'),
    path('experience/register/', views.work_experience_register_view, name='work_experience_register'),
    path('login/', views.user_login, name='login'),
    path('welcome/', views.welcome, name='welcome'),
]
