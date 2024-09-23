from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/freelancer/', views.freelancer_signup, name='register_freelancer'),
    
    path('signup/client/', views.client_signup, name='client_signup'),
    
    # URL para registro académico
    path('education/register/', views.education_register_view, name='education_register'),
    
    # URL para registro de experiencia laboral
    path('work-experience/register/', views.work_experience_register_view, name='work_experience_register'),
    
    # URL para registrar certificaciones
    path('certification/register/', views.certification_register_view, name='certification_register'),
    
    # URL para registrar enlaces de portafolio
    path('portfolio/register/', views.portfolio_register_view, name='portfolio_register'),
    
    path('languages/register/', views.register_languages_view, name='register_languages'),
     
    path('skills/register/', views.register_skills_view, name='register_skills'),
    
    # URL para login
    path('login/', views.user_login, name='login'),
    
    # URL de bienvenida
    path('welcome/', views.welcome, name='welcome'),
    
    # Home para freelancers DASHBOARD
    path("Home-Freelancer/", views.home_freelancer, name="home_freelancer"),
    
    # URL para cambiar contraseña
    path("ChangePassword/", views.change_password, name="change_password"),

    # Configuración de perfil
    path("profileSettings/", views.profile_settings, name="profile_settings"),
    
    # Búsqueda de freelancers
    path('search/', views.search_freelancers, name='search_freelancers'),
    
    # Perfil de freelancer
    path('freelancer/<int:id>/', views.freelancer_profile, name='freelancer_profile'),
    
    # Búsqueda de clientes
    path('search_clients/', views.search_clients, name='search_clients'),
    
    # Perfil de cliente
    path('client/<int:id>/', views.client_profile, name='client_profile'),
    
]