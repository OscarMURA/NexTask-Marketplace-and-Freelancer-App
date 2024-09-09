from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('signup/freelancer/', views.freelancer_signup, name='register_freelancer'),
    path('signup/client/', views.client_signup, name='client_signup'),
    path('login/', views.user_login, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('register/education/', views.education_register,name='education_register'),
    path('register/workexperience/', views.workexperience_register, name='workexperience_register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('home/', views.home, name='home'),
]
