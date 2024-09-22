from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('createProject/', views.create_project, name='createProject'),
    path("home-Client/", views.home_client, name="home_client"),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
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

]