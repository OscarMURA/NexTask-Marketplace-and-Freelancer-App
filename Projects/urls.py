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
]