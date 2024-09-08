from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include



urlpatterns = [
    path('signup/freelancer/', views.freelancer_signup, name='register_freelancer'),
    path('signup/client/', views.client_signup, name='client_signup'),
    path('login/', views.login, name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')), #Agregamos esta línea
    path('', views.home, name='home'),

]
