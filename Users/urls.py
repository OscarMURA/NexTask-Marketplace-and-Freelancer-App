from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

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
    
    path("Home-Client/", views.home_client, name="home_client"),

    path("Home-Freelancer/", views.home_freelancer, name="home_freelancer"),
    
    path("CreateProject/", views.createProject, name="createProject"),
    
    path("ChangePassword/", views.change_password, name="change_password"),

]

