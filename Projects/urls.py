from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('createProject/', views.create_project, name='createProject'),
    path("home-Client/", views.home_client, name="home_client"),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),

    # Milestones
    path('projects/<int:project_id>/add_milestone/', views.create_milestone, name='add_milestone'),
    path('milestones/<int:milestone_id>/edit/', views.edit_milestone, name='edit_milestone'),
    path('milestone/<int:pk>/', views.milestone_detail_view, name='milestone_detail'),
    path('delete_milestone/<int:milestone_id>/', views.delete_milestone, name='delete_milestone'),

    path('milestone/<int:milestone_id>/add_task/', views.create_task, name='create_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    
    path('projects/<int:project_id>/search_freelancer/', views.search_freelancer, name='search_freelancer'),
    path('contract/<int:project_id>/<int:freelancer_id>/', views.freelancer_profile, name='freelancer_profile'),

    path('project/<int:project_id>/freelancer/<int:freelancer_id>/contract/', views.create_project_freelancer_association, name='create_project_freelancer_association'),
    path('projects/<int:project_id>/applications/', views.manage_applications, name='manage_applications'),


    path('view_freelancer_profile//<int:project_id>/<int:freelancer_id>/', views.freelancer_profile_manage, name='view_freelancer_profile_manage'),

    # Search and Apply to Projects
    path('search_projects/', views.search_projects, name='search_projects'),  # New URL for project search
    path('project/view/<int:project_id>/', views.view_project_search, name='view_project_search'),
    path('project/apply/<int:project_id>/', views.apply_to_project, name='apply_to_project'),
    path('application-confirmation/', views.application_confirmation, name='application_confirmation'),
    
    path('freelancer/project/<int:project_id>/', views.project_detail_freelancer, name='project_detail_freelancer'),

    path('milestone/<int:pk>/details/', views.milestone_detail_view_freelancer, name='milestone_detail_freelancer'),
    
    path('tasks/<int:task_id>/edit/',views.edit_task_freelancer, name='edit_task_freelancer'),

    path('tasks/<int:task_id>/', views.task_detail_view_freelancer, name='task_detail_freelancer'),

    path('projects/freelancer/manage_applications/', views.manage_applications_freelancer, name='manage_applications_freelancer'),
    
    path('projects/<int:project_id>/freelancers/',  views.freelancers_in_project, name='freelancers_in_project'),


]
