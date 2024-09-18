from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('createProject/', views.create_project, name='createProject'),
    path("home-Client/", views.home_client, name="home_client"),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),

] 