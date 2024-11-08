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

    # URL for changing password client
    path("changePasswordClient/", views.change_password_client, name="change_password_client"),

    # URL for changing password freelancer
    path("changePasswordFreelancer/", views.change_password_freelancer, name="change_password_freelancer"),

    # URL for password recovery
    path("passwordRecovery/", views.password_recovery, name="password_recovery"),

    # URL for verfy code validation email
    path('verify_code/<int:user_id>/', views.verify_code, name='verify_code'),

    # URL for password reset
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),

    # URL for profile settings freelancer
    path("profileSettingsFreelancer/", views.profile_settings_freelancer, name="profile_settings_freelancer"),

    # URL for profile settings client
    path("profileSettingsClient/", views.profile_settings_client, name="profile_settings_client"),

    # URL for searching freelancers
    path('search/', views.search_freelancers, name='search_freelancers'),

    # URL for viewing a freelancer's profile
    path('freelancer/<int:id>/', views.freelancer_profile, name='freelancer_profile'),

    # URL for searching clients
    path('search_clients/', views.search_clients, name='search_clients'),

    # URL for viewing a client's profile
    path('client/<int:id>/', views.client_profile, name='client_profile'),

]

