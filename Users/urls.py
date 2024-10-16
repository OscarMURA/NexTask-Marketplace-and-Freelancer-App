from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URL for freelancer signup
    path('signup/freelancer/', views.freelancer_signup, name='register_freelancer'),

    # URL for client signup
    path('signup/client/', views.client_signup, name='client_signup'),

    # URL for registering education information
    path('education/register/', views.education_register_view, name='education_register'),

    # URL for registering work experience
    path('work-experience/register/', views.work_experience_register_view, name='work_experience_register'),

    # URL for registering certifications
    path('certification/register/', views.certification_register_view, name='certification_register'),

    # URL for registering portfolio links
    path('portfolio/register/', views.portfolio_register_view, name='portfolio_register'),

    # URL for registering languages
    path('languages/register/', views.register_languages_view, name='register_languages'),

    # URL for registering skills
    path('skills/register/', views.register_skills_view, name='register_skills'),

    # URL for user login
    path('login/', views.user_login, name='login'),

    # URL for welcome page
    path('welcome/', views.welcome, name='welcome'),

    # Home page for freelancers (dashboard)
    path("Home-Freelancer/", views.home_freelancer, name="home_freelancer"),

    # URL for changing password
    path("ChangePassword/", views.change_password, name="change_password"),

    # URL for profile settings freelancer
    path("profileSettingsFreelancer/", views.profile_settings_freelancer, name="profile_settings_freelancer"),

    # URL for searching freelancers
    path('search/', views.search_freelancers, name='search_freelancers'),

    # URL for viewing a freelancer's profile
    path('freelancer/<int:id>/', views.freelancer_profile, name='freelancer_profile'),

    # URL for searching clients
    path('search_clients/', views.search_clients, name='search_clients'),

    # URL for viewing a client's profile
    path('client/<int:id>/', views.client_profile, name='client_profile'),

]

