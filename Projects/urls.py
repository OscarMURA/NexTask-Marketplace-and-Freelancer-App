from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    # Function to create a new project
    path('createProject/', views.create_project, name='createProject'),  
    
    # Function to view the client's home page
    path("home-Client/", views.home_client, name="home_client"),  
    
    # Function to view project details
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),  
    
    # Function to edit an existing project
    path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'),  
    
    # Function to delete a project
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),  

    # Milestones
    # Function to add a milestone to a project
    path('projects/<int:project_id>/add_milestone/', views.create_milestone, name='add_milestone'),  
    
    # Function to edit a milestone
    path('milestones/<int:milestone_id>/edit/', views.edit_milestone, name='edit_milestone'),  
    
    # Function to view milestone details
    path('milestone/<int:pk>/', views.milestone_detail_view, name='milestone_detail'),  
    
    # Function to delete a milestone
    path('delete_milestone/<int:milestone_id>/', views.delete_milestone, name='delete_milestone'),  

    # Tasks
    # Function to create a task for a milestone
    path('milestone/<int:milestone_id>/add_task/', views.create_task, name='create_task'),  
    
    # Function to edit an existing task
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),  
    
    # Function to delete a task
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),  
    
    # Function to view task details
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),  
    
    # Freelancer search and profiles
    # Function to search for freelancers in a project
    path('projects/<int:project_id>/search_freelancer/', views.search_freelancer, name='search_freelancer'),  
    
    # Function to view freelancer's profile
    path('contract/<int:project_id>/<int:freelancer_id>/', views.freelancer_profile, name='freelancer_profile'),  

    # Function to create a project-freelancer association
    path('project/<int:project_id>/freelancer/<int:freelancer_id>/contract/', views.create_project_freelancer_association, name='create_project_freelancer_association'),  
    
    # Function to manage freelancer applications for a project
    path('projects/<int:project_id>/applications/', views.manage_applications, name='manage_applications'),  

    # Function to manage freelancer's profile view
    path('view_freelancer_profile/<int:project_id>/<int:freelancer_id>/', views.freelancer_profile_manage, name='view_freelancer_profile_manage'),  

    # Search and Apply to Projects
    # Function for searching projects
    path('search_projects/', views.search_projects, name='search_projects'),  
    
    # Function to view a public project
    path('project/view/<int:project_id>/', views.view_project_search, name='view_project_search'),  
    
    # Function to apply to a project
    path('project/apply/<int:project_id>/', views.apply_to_project, name='apply_to_project'),  
    
    # Function for application confirmation
    path('application-confirmation/', views.application_confirmation, name='application_confirmation'),  
    
    # Freelancer-specific project views
    # Function to view a project from the freelancer's perspective
    path('freelancer/project/<int:project_id>/', views.project_detail_freelancer, name='project_detail_freelancer'),  
    
    # Function to view milestone details for freelancers
    path('milestone/<int:pk>/details/', views.milestone_detail_view_freelancer, name='milestone_detail_freelancer'),  
    
    # Function to edit a task for freelancers
    path('tasks/<int:task_id>/edit/', views.edit_task_freelancer, name='edit_task_freelancer'),  
    
    # Function to view task details for freelancers
    path('freelancer/task/<int:task_id>/', views.task_detail_view_freelancer, name='task_detail_freelancer'),  
    
    # Function to manage freelancer applications
    path('projects/freelancer/manage_applications/', views.manage_applications_freelancer, name='manage_applications_freelancer'),  
    
    # Function to view freelancers associated with a specific project
    path('projects/<int:project_id>/freelancers/', views.freelancers_in_project, name='freelancers_in_project'), 
    
    path('projects/deleted/', views.deleted_projects, name='deleted_projects'),
    path('projects/<int:project_id>/restore/', views.restore_project, name='restore_project'),
    path('projects/<int:project_id>/permanent_delete/', views.permanently_delete_project, name='permanent_delete_project'),
    
    path('milestones/<int:project_id>/deleted/', views.deleted_milestones, name='deleted_milestones'),
    path('milestones/<int:milestone_id>/restore/', views.restore_milestone, name='restore_milestone'),
    path('milestones/<int:milestone_id>/permanent_delete/', views.permanently_delete_milestone, name='permanent_delete_milestone'),
    
    path('tasks/<int:milestone_id>/deleted/', views.deleted_tasks, name='deleted_tasks'),
    path('tasks/<int:task_id>/restore/', views.restore_task, name='restore_task'),
    path('tasks/<int:task_id>/permanent_delete/', views.permanently_delete_task, name='permanent_delete_task'),

    path('redirect-to-payments/', views.redirect_to_client_payment_history, name='redirect_to_client_payments'),
    path('redirect-to-payments/', views.redirect_to_freelancer_payment_history, name='redirect_to_freelancer_payments'),

]
