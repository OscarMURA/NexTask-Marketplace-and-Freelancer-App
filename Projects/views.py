# views.py
from django.shortcuts import render, redirect, get_object_or_404

from Notifications.models import Notification
from .forms import ProjectForm
from Users.models import ClientProfile  # Asegúrate de importar ClientProfile

from django.utils.translation import gettext as _
from .models import *
from django.urls import reverse
from django.contrib import messages
from .models import Project, Milestone,Task
from .forms import MilestoneForm, TaskForm
from django.db.models import Q
from Users.models import FreelancerProfile, Skill, Language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib import messages
from django.utils import timezone
from Comments.forms import CommentForm
from Comments.models import Comment
from django.http import HttpRequest, HttpResponse
import random
from Reports.views import client_report_view, generate_report_view
from Reports.forms import ReportFilterForm
from Reports.views import get_client_report_context, get_generate_report_context


def create_project(request):
    """
    Create a new project.

    If the request method is POST, the function processes the submitted form data.
    If the form is valid, a new project is created and saved with the client profile
    of the authenticated user. The user is redirected to the home client page.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        HttpResponse: Renders the 'createProject.html' template with the form context 
        or redirects to the home client page on success.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user.clientprofile  
            project.save()
            print(project.category)
            print("Proyecto creado", project)  # Print the created project
            return redirect('home_client')  # Redirect to the project list or success page
        else:
            print("Error en el formulario", form.errors)
    else:
        form = ProjectForm()

    return render(request, 'Projects/createProject.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project
from Payments.models import Payment
import random

@login_required
def home_client(request):
    """
    Display the home page for the client.

    Retrieves all projects associated with the client's profile, 
    the total number of projects, total budget, and payment statuses.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'homeClient.html' template with project, budget, and payment information.
    """
    client_profile = request.user.clientprofile
    projects = client_profile.projects.all()
    total_projects = projects.count()
    total_balance = client_profile.get_total_budget()

    # Count pending and completed payments for the client's projects
    pending_payments_count = Payment.objects.filter(client=client_profile, status='pending').count()
    completed_payments_count = Payment.objects.filter(client=client_profile, status='paid').count()

    # List of colors for project events
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F0A500', '#8E44AD', '#1ABC9C', '#E74C3C', '#3498DB']

    # Creating events with assigned colors
    events = [
        {
            'title': project.title,
            'start': project.start_date.isoformat(),
            'end': project.due_date.isoformat(),
            'color': random.choice(colors)
        }
        for project in projects
    ]

    client_report_data = get_client_report_context(request)
    generate_report_data = get_generate_report_context(request)

    context = {
        'projects': projects,
        'total_projects': total_projects,
        'total_balance': total_balance,
        'pending_payments_count': pending_payments_count,
        'completed_payments_count': completed_payments_count,
        'events_json': events,
        'form': client_report_data.get('form'),
        **client_report_data,
        **generate_report_data,
    }

    return render(request, 'Projects/homeClient.html', context)



@login_required
def project_detail(request, project_id):
    """
    Retrieve and display the details of a specific project along with its milestones and tasks.
    """
    project = get_object_or_404(Project, pk=project_id)
    milestones = project.milestones.all()
    # Puedes agregar aquí la lógica de tareas si quieres mostrar también las tareas dentro de los hitos
    tasks = Task.objects.filter(milestone__project=project)

    # Lista de colores para los hitos
    colors = ['#FF5733', '#33FF57', '#3357FF', '#F0A500', '#8E44AD', '#1ABC9C', '#E74C3C', '#3498DB']

    # Lógica para renderizar los hitos en FullCalendar
    timeline_data = [
        {
            'title': milestone.title,
            'start': milestone.start_date.isoformat(),  # Use ISO format for the date
            'end': milestone.due_date.isoformat(),  # Also convert due date to ISO format
            'milestone': milestone.title,
            'color': random.choice(colors)  # Asignar un color aleatorio de la lista
        }
        for milestone in milestones
    ]
    
    context = {
        'project': project,
        'timeline_data': timeline_data,
        'milestones': milestones,
        'tasks': tasks,  # Si es necesario mostrar las tareas asociadas
    }
    return render(request, 'Projects/project_detail.html', context)
    project = get_object_or_404(Project, id=project_id)
    milestones = project.milestones.all().filter(is_deleted=False)

    return render(request, 'Projects/project_detail.html', {
        'project': project,
        'milestones': milestones,
    })

def edit_project(request, project_id):
    """
    Edit an existing project.

    Retrieves the project based on the provided ID. If the request method is POST,
    it processes the submitted form data. If the form is valid, the project is updated
    and the user is redirected to the project detail page.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to be edited.

    Returns:
        HttpResponse: Renders the 'edit_project.html' template with the form context 
        or redirects to the project detail page on success.
    """
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)  # Redirect to project details
    else:
        form = ProjectForm(instance=project)

    return render(request, 'Projects/edit_project.html', {'form': form, 'project': project})

def delete_project(request, project_id):
    """
    Delete a specific project.

    Retrieves the project using the provided ID. If the request method is POST,
    the project is deleted and a success message is displayed. The user is then 
    redirected to the home client page.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to be deleted.

    Returns:
        HttpResponse: Redirects to the home client page after deletion.
    """
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.is_deleted = True
        project.save()
        messages.success(request, "Proyecto eliminado exitosamente")
        return redirect('home_client') 

    return redirect(reverse('home_client'))

def create_milestone(request, project_id):
    """
    Create a new milestone for a specific project.

    Retrieves the project based on the provided ID. If the request method is POST,
    it processes the submitted form data to create a new milestone. The user is 
    redirected to the project detail page on success.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to which the milestone is associated.

    Returns:
        HttpResponse: Renders the 'create_milestone.html' template with the form context 
        or redirects to the project detail page on success.
    """
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = MilestoneForm(request.POST, request.FILES)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = MilestoneForm()

    return render(request, 'Projects/create_milestone.html', {'form': form, 'project': project})

def edit_milestone(request, milestone_id):
    """
    Edit an existing milestone.

    Retrieves the milestone using the provided ID. If the request method is POST,
    it processes the submitted form data to update the milestone. The user is 
    redirected to the project detail page on success.

    Args:
        request (HttpRequest): The HTTP request object.
        milestone_id (int): The ID of the milestone to be edited.

    Returns:
        HttpResponse: Renders the 'edit_milestone.html' template with the form context 
        or redirects to the project detail page on success.
    """
    milestone = get_object_or_404(Milestone, id=milestone_id)

    if request.method == 'POST':
        form = MilestoneForm(request.POST, request.FILES, instance=milestone)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=milestone.project.id)
    else:
        form = MilestoneForm(instance=milestone)

    return render(request, 'Projects/edit_milestone.html', {'form': form, 'milestone': milestone})

def milestone_detail_view(request, pk):
    """
    Retrieve and display the details of a specific milestone.

    Uses the milestone ID to get the milestone from the database and renders it 
    in the 'milestone_detail.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The ID of the milestone to be retrieved.

    Returns:
        HttpResponse: Renders the 'milestone_detail.html' template with the milestone context.
    """
    milestone = get_object_or_404(Milestone, pk=pk)
    tasks = milestone.tasks.all()
    # Asignar colores basados en el estado de la tarea
    color_map = {
        'pending': '#FFC107',  # Amarillo para tareas pendientes
        'in_progress': '#007BFF',  # Azul para tareas en progreso
        'completed': '#28A745',  # Verde para tareas completadas
    }

    # Datos para FullCalendar
    timeline_data = [
        {
            'title': task.title,
            'start': task.start_date.isoformat(),
            'end': task.due_date.isoformat() if task.due_date else task.start_date.isoformat(),
            'description': task.title,
            'color': color_map.get(task.status, '#378006'),  # Asignar color según el estado o usar uno por defecto
        }
        for task in tasks
    ]
    
    context = {
        'milestone': milestone,
        'tasks': tasks,
        'timeline_data': timeline_data,
    }
    return render(request, 'Projects/milestone_detail.html', context)
    tasks = milestone.tasks.all().filter(is_deleted=False)
    return render(request, 'Projects/milestone_detail.html', {'milestone': milestone, 'tasks': tasks})

def delete_milestone(request, milestone_id):
    """
    Delete a specific milestone.

    Retrieves the milestone using the provided ID. If the request method is POST,
    the milestone is deleted and a success message is displayed. The user is then 
    redirected to the project detail page.

    Args:
        request (HttpRequest): The HTTP request object.
        milestone_id (int): The ID of the milestone to be deleted.

    Returns:
        HttpResponse: Redirects to the project detail page after deletion.
    """
    milestone = get_object_or_404(Milestone, id=milestone_id)

    if request.method == "POST":
        milestone.is_deleted = True
        milestone.save()
        messages.success(request, "Milestone eliminado exitosamente")
        return redirect('project_detail', project_id=milestone.project.id)

    return redirect(reverse('home_client'))

def create_task(request, milestone_id):
    """
    Create a new task for a specific milestone.

    Retrieves the milestone using the provided ID. If the request method is POST,
    it processes the submitted form data to create a new task. The user is redirected 
    to the milestone detail page on success.

    Args:
        request (HttpRequest): The HTTP request object.
        milestone_id (int): The ID of the milestone to which the task is associated.

    Returns:
        HttpResponse: Renders the 'create_task.html' template with the form context 
        or redirects to the milestone detail page on success.
    """
    milestone = get_object_or_404(Milestone, id=milestone_id)
    project = milestone.project  # Get the project associated with the milestone

    # Get all freelancers with an active contract in this project
    active_contracts = Contract.objects.filter(project=project, status='active')
    freelancers = [contract.freelancer for contract in active_contracts]
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, freelancers=freelancers)  # Pass freelancers to the form
        if form.is_valid():
            task = form.save(commit=False)
            task.milestone = milestone  # Associate the task with the milestone
            task.save()
            return redirect('milestone_detail', pk=milestone.id)
    else:
        form = TaskForm(freelancers=freelancers)  # Pass freelancers to the form

    return render(request, 'Projects/create_task.html', {
        'form': form,
        'milestone': milestone,
    })

def edit_task(request, task_id):
    """
    Edit an existing task.

    Retrieves the task using the provided ID. If the request method is POST,
    it processes the submitted form data to update the task. The user is redirected 
    to the milestone detail page on success.

    Args:
        request (HttpRequest): The HTTP request object.
        task_id (int): The ID of the task to be edited.

    Returns:
        HttpResponse: Renders the 'edit_task.html' template with the form context 
        or redirects to the milestone detail page on success.
    """
    task = get_object_or_404(Task, id=task_id)
    milestone = task.milestone  # Get the associated milestone
    project = milestone.project  # Get the associated project

    # Get all freelancers with an active contract in this project
    active_contracts = Contract.objects.filter(project=project, status='active')
    freelancers = [contract.freelancer for contract in active_contracts]

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('milestone_detail', pk=task.milestone.id)
    else:
        form = TaskForm(instance=task)

    # Override the queryset of the assigned_to field to show only freelancers with active contracts
    form.fields['assigned_to'].queryset = FreelancerProfile.objects.filter(id__in=[freelancer.id for freelancer in freelancers])

    return render(request, 'Projects/edit_task.html', {
        'form': form,
        'task': task
    })

def delete_task(request, task_id):
    """
    Delete a specific task.

    Retrieves the task using the provided ID. If the request method is POST,
    the task is deleted and a success message is displayed. The user is then 
    redirected to the milestone detail page.

    Args:
        request (HttpRequest): The HTTP request object.
        task_id (int): The ID of the task to be deleted.

    Returns:
        HttpResponse: Redirects to the milestone detail page after deletion.
    """
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.is_deleted = True
        task.save()
        messages.success(request, "Tarea eliminada exitosamente.")
        return redirect('milestone_detail', pk=task.milestone.id)

    return redirect('milestone_detail', pk=task.milestone.id)

def task_detail(request, task_id):
    """
    Recupera y muestra los detalles de una tarea específica para un cliente.
    Permite a los clientes y a los freelancers asociados agregar comentarios a la tarea.
    """
    task = get_object_or_404(Task, id=task_id)
    
    context = {'task': task}

    comments_context = handle_comments(request, task, request.user)
    print("Comentarios Contexto:", comments_context)  # Línea de depuración

    
    if 'redirect' in comments_context and comments_context['redirect']:
        return redirect(request.path)  # Redirige a la misma página después de un POST exitoso

    context.update(comments_context)
    return render(request, 'Projects/task_detail.html', context)

def search_freelancer(request, project_id):
    """
    Search for freelancers based on specified criteria.

    Retrieves the project using the provided ID and filters freelancers
    based on query parameters (skills, languages, country). The search results
    are rendered in the 'search_freelancer.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project for which freelancers are being searched.

    Returns:
        HttpResponse: Renders the 'search_freelancer.html' template with search results.
    """
    project = get_object_or_404(Project, id=project_id)

    freelancers = FreelancerProfile.objects.all()
    skills = Skill.objects.all()
    languages = Language.objects.all()
    countries = FreelancerProfile.objects.values_list('country', flat=True).distinct()

    # Filter by search parameters
    query = request.GET.get('q')
    selected_skill = request.GET.get('skills')
    selected_language = request.GET.get('languages')
    selected_country = request.GET.get('country')

    if query:
        freelancers = freelancers.filter(
            Q(user__username__icontains=query) |
            Q(skills__name__icontains=query) |
            Q(country__icontains=query) |
            Q(languages__language__icontains=query)
        ).distinct()

    if selected_skill:
        freelancers = freelancers.filter(skills__id=selected_skill).distinct()

    if selected_language:
        freelancers = freelancers.filter(languages__id=selected_language).distinct()

    if selected_country:
        freelancers = freelancers.filter(country=selected_country).distinct()

    context = {
        'project': project,  # Ensure the project is passed to the context
        'freelancers': freelancers,
        'skills': skills,
        'languages': languages,
        'countries': countries,
    }

    return render(request, 'Projects/search_freelancer.html', context)

def freelancer_profile(request, project_id, freelancer_id):
    """
    Retrieve and display the profile of a specific freelancer.

    Uses the project and freelancer IDs to get the relevant data and renders
    it in the 'freelancer_profile.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project associated with the freelancer.
        freelancer_id (int): The ID of the freelancer to be retrieved.

    Returns:
        HttpResponse: Renders the 'freelancer_profile.html' template with the freelancer context.
    """
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, user__id=freelancer_id)

    context = {
        'project': project,
        'freelancer': freelancer,
    }

    return render(request, 'Projects/freelancer_profile.html', context)

def create_project_freelancer_association(request, project_id, freelancer_id):
    """
    Create an association between a project and a freelancer.

    Retrieves the project and freelancer using the provided IDs. If the freelancer
    is not already associated with the project, a new association is created. 
    The user is then redirected to the project detail page.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project.
        freelancer_id (int): The ID of the freelancer.

    Returns:
        HttpResponse: Redirects to the project detail page after creating the association.
    """
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, user__id=freelancer_id)

    # Create the association between the project and freelancer
    association, created = ProjectFreelancer.objects.get_or_create(
        project=project,
        freelancer=freelancer,
        defaults={'status': 'pending'}
    )
    
    if created:
        messages.success(request, f"Contract pending for {freelancer.user.username} on project {project.title}")
    else:
        messages.info(request, f"A contract already exists for {freelancer.user.username} on project {project.title}")

    return redirect('project_detail', project_id=project.id)

def manage_applications(request, project_id):
    """
    Manage freelancer applications for a specific project.

    Retrieves all applications associated with the project. If the request method
    is POST, it processes the action (accept or reject) on the selected application.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project for which applications are being managed.

    Returns:
        HttpResponse: Renders the 'manageApplications.html' template with applications context.
    """
    project = get_object_or_404(Project, id=project_id)
    applications = Application.objects.filter(project=project)

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        application = get_object_or_404(Application, id=application_id)

        if action == 'accept':
            # Create the contract
            Contract.objects.create(
                project=application.project,
                freelancer=application.freelancer
            )

            Notification.objects.create(
                recipient=application.freelancer.user,  # El usuario que hizo la aplicación
                message=_("Your application for the project '%(project_title)s' has been accepted.") % {
                    'project_title': application.project.title
                },
                created_at=timezone.now()  # No es necesario si ya tienes el valor predeterminado en el modelo
            )

            # Delete the application after accepting
            application.delete()
            messages.success(request, f"Freelancer {application.freelancer.user.username} accepted and contract created.")
            return redirect('home_client')

        elif action == 'reject':
            application.delete()  # Delete the application when rejected
            messages.info(request, f"Freelancer {application.freelancer.user.username} rejected.")
            return redirect('home_client')

    return render(request, 'projects/manageApplications.html', {
        'project': project,
        'applications': applications,
    })


@login_required
def search_projects(request):
    """
    Search for projects based on specified criteria.

    Retrieves projects from the database and filters them based on the user's 
    search query and selected category. The search results are rendered in 
    the 'search_projects_freelancer_dashboard.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'search_projects_freelancer_dashboard.html' template with search results.
    """
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    projects = Project.objects.all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(client__user__username__icontains=query)
        )

    if category_filter and category_filter != 'all':
        projects = projects.filter(category=category_filter)

    return render(request, 'Projects/search_projects_freelancer_dashboard.html', {
        'projects': projects,
        'categories': Project.CATEGORY_CHOICES,
        'selected_category': category_filter,
    })

@login_required
def view_project_search(request, project_id):
    """
    Retrieve and display the details of a specific project.

    Uses the project ID to get the project from the database and renders it 
    in the 'view_project_search_freelancer_dashboard.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to be retrieved.

    Returns:
        HttpResponse: Renders the 'view_project_search_freelancer_dashboard.html' template with the project context.
    """
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'Projects/view_project_search_freelancer_dashboard.html', {'project': project})

@login_required
def apply_to_project(request, project_id):
    """
    Submit an application to a specific project.

    Retrieves the project using the provided ID. If the user does not have 
    a freelancer profile, they are redirected to the registration page. 
    If the application is created, the user is redirected to the application confirmation page.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to which the application is being submitted.

    Returns:
        HttpResponse: Redirects to the application confirmation page after applying.
    """
    project = get_object_or_404(Project, id=project_id)

    if not hasattr(request.user, 'freelancer_profile'):
        return redirect('register_freelancer')

    application, created = Application.objects.get_or_create(
        freelancer=request.user.freelancer_profile, project=project
    )

    return redirect('application_confirmation')

def application_confirmation(request):
    """
    Display the application confirmation page.

    Renders the 'application_confirmation.html' template, indicating 
    that the application was successfully submitted.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'application_confirmation.html' template.
    """
    return render(request, 'Projects/application_confirmation.html')

@login_required
def search_public_projects(request):
    """
    Search for public projects based on a query.

    Retrieves projects from the database and filters them based on the user's 
    search query. The search results are rendered in the 'search_projects.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'search_projects.html' template with search results.
    """
    query = request.GET.get('q')
    projects = Project.objects.all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(client__user__username__icontains=query)
        )

    return render(request, 'Projects/search_projects.html', {
        'projects': projects,
    })

@login_required
def view_public_project(request, project_id):
    """
    Retrieve and display the details of a public project.

    Uses the project ID to get the project from the database and renders it 
    in the 'view_project_search.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to be retrieved.

    Returns:
        HttpResponse: Renders the 'view_project_search.html' template with the project context.
    """
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'Projects/view_project_search.html', {'project': project})

def freelancer_profile_manage(request, project_id, freelancer_id):
    """
    Retrieve and display the profile of a specific freelancer for a project.

    Uses the project and freelancer IDs to get the relevant data and renders
    it in the 'freelancer_profile_manage.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project associated with the freelancer.
        freelancer_id (int): The ID of the freelancer to be retrieved.

    Returns:
        HttpResponse: Renders the 'freelancer_profile_manage.html' template with the freelancer context.
    """
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, user__id=freelancer_id)

    context = {
        'project': project,
        'freelancer': freelancer,
    }

    return render(request, 'Projects/freelancer_profile_manage.html', context)

def project_detail_freelancer(request, project_id):
    """
    Retrieve and display the details of a project for a freelancer.

    Uses the project ID to get the project from the database and renders it 
    in the 'project_detail_freelancer.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project to be retrieved.

    Returns:
        HttpResponse: Renders the 'project_detail_freelancer.html' template with the project context.
    """
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'Projects/project_detail_freelancer.html', {'project': project})

def milestone_detail_view_freelancer(request, pk):
    """
    Retrieve and display the details of a milestone for a freelancer.

    Uses the milestone ID to get the milestone from the database and filters
    tasks associated with the freelancer. If the freelancer profile does not exist,
    a suitable template is rendered.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The ID of the milestone to be retrieved.

    Returns:
        HttpResponse: Renders the 'milestone_detail_freelancer.html' template with the milestone and task context.
    """
    milestone = get_object_or_404(Milestone, pk=pk)

    # Access the freelancer profile using the related_name
    try:
        freelancer_profile = request.user.freelancer_profile  # Accessing the freelancer profile
    except FreelancerProfile.DoesNotExist:
        return render(request, 'Projects/no_profile.html')  # Render an appropriate template

    # Filter tasks only for the freelancer
    #tasks = milestone.tasks.filter(assigned_to=freelancer_profile)
    tasks = milestone.tasks.all()

    return render(request, 'Projects/milestone_detail_freelancer.html', {
        'milestone': milestone,
        'tasks': tasks,
    })

def edit_task_freelancer(request, task_id):
    """
    Edit an existing task assigned to a freelancer.

    Retrieves the task using its ID and checks if the current user is authorized
    to edit it. If the form is valid, the task is updated and the user is redirected 
    to the milestone details.

    Args:
        request (HttpRequest): The HTTP request object.
        task_id (int): The ID of the task to be edited.

    Returns:
        HttpResponse: Renders the 'edit_task_freelancer.html' template with the form context
                       or redirects to the milestone detail if successful.
    """
    task = get_object_or_404(Task, id=task_id)
    milestone = task.milestone  # Retrieve the associated milestone
    project = milestone.project  # Retrieve the associated project

    # Retrieve the freelancer's profile
    freelancer_profile = request.user.freelancer_profile

    # Filter tasks only for the freelancer
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('milestone_detail_freelancer', pk=milestone.id)  # Redirect to the freelancer's milestones
    else:
        form = TaskForm(instance=task)

    return render(request, 'Projects/edit_task_freelancer.html', {
        'form': form,
        'task': task
    })

def task_detail_view_freelancer(request, task_id):
    """
    Recupera y muestra los detalles de una tarea específica para un freelancer.
    Permite a los freelancers y al cliente agregar comentarios a la tarea.
    """
    task = get_object_or_404(Task, id=task_id)
    context = {'task': task} 

    comments_context = handle_comments(request, task, request.user)
    print("Comentarios Contexto:", comments_context)  # Línea de depuración

    
    if 'redirect' in comments_context and comments_context['redirect']:
        return redirect(request.path)  # Redirige a la misma página después de un POST exitoso

    context.update(comments_context)
    return render(request, 'Projects/task_detail_freelancer.html', context)

def manage_applications_freelancer(request):
    """
    Manage freelancer applications for projects.

    Retrieves all pending applications for the current freelancer. 
    Depending on the user's action, the application can be accepted or rejected. 
    If accepted, a contract is created, and the application is deleted.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'manage_applications_freelancer.html' template 
                       with the applications context or redirects based on user actions.
    """
    # Filter applications where the freelancer is the current user
    applications = ProjectFreelancer.objects.filter(freelancer=request.user.freelancer_profile, status='pending')

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(ProjectFreelancer, id=application_id)

        if action == 'accept':
            # Check if a contract already exists
            if not Contract.objects.filter(project=application.project, freelancer=application.freelancer).exists():
                # Create the contract
                Contract.objects.create(project=application.project, freelancer=application.freelancer)

                # Obtener el nombre y apellido del usuario que acepta la aplicación
                accepting_user = request.user  # El usuario que acepta la aplicación

                message = _("Your application for the project '%(project_title)s' has been accepted by %(freelancer_name)s.") % {
                    'project_title': application.project.title,
                    'freelancer_name': f"{accepting_user.first_name} {accepting_user.last_name}"
                }

                Notification.objects.create(
                    recipient=application.project.client.user,  # Suponiendo que 'user' es el campo que representa al cliente
                    message=message,
                    created_at=timezone.now()  # No es necesario si ya tienes el valor predeterminado en el modelo
                )
                print("Notificación creada con éxito")  # Mensaje de depuración
                print("-----------------------------")

            else:
                # Notify that the contract already exists (implement as desired)
                pass
            
            application.delete()  # Delete the application after acceptance

        elif action == 'reject':
            application.delete()  # Delete the application upon rejection

        return redirect('manage_applications_freelancer')

    return render(request, 'Projects/manage_applications_freelancer.html', {
        'applications': applications,
    })

def freelancers_in_project(request, project_id):
    """
    Retrieve and display all freelancers associated with a specific project.

    Uses the project ID to get the project from the database and filters 
    freelancers who have contracts related to that project.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project for which freelancers are being retrieved.

    Returns:
        HttpResponse: Renders the 'freelancers_in_project.html' template with the project 
                       and freelancers context.
    """
    project = get_object_or_404(Project, id=project_id)
    freelancers = Contract.objects.filter(project=project)

    return render(request, 'Projects/freelancers_in_project.html', {
        'project': project,
        'freelancers': freelancers,
    })

def handle_comments(request, task, user):
    print(f"Manejando comentarios para la tarea: {task.title}")
    project = task.milestone.project


    # Obtener todos los comentarios existentes ordenados por fecha de creación
    comments = task.comments.all().order_by('created_at')

    # Implementar Paginación: 5 comentarios por página
    paginator = Paginator(comments, 5)  # 5 comentarios por página
    page = request.GET.get('page')

    try:
        comments_paginated = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, muestra la primera página
        comments_paginated = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, muestra la última página
        comments_paginated = paginator.page(paginator.num_pages)

    # Manejar el formulario de comentario
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print("Form is bound:", form.is_bound)
        if form.is_valid():
            # Crear y guardar el comentario
            comment = form.save(commit=False)
            comment.task = task
            comment.author = user
            comment.save()
            print("Comentario guardado exitosamente.")
            # Redirigir a la misma página para evitar reenvío del formulario
            return {'redirect': True}
        else:
            print("Errores en el formulario:", form.errors)
    else:
        form = CommentForm()

    print("Comentarios Contexto:", {'comments': comments_paginated, 'form': form})
    return {
        'comments': comments_paginated,
        'form': form,
        'paginator': paginator,
        'page_obj': comments_paginated,
        'is_paginated': comments_paginated.has_other_pages(),
    }
    
def restore_project(request, project_id):
    """
    Restaura un proyecto eliminado.
    """
    project = get_object_or_404(Project.all_objects, id=project_id, is_deleted=True)

    if request.method == "POST":
        project.is_deleted = False
        project.save()
        messages.success(request, "Proyecto restaurado exitosamente")
        return redirect('home_client') 

    return redirect(reverse('deleted_projects'))

def permanently_delete_project(request, project_id):
    """
    Elimina permanentemente un proyecto.
    """
    project = get_object_or_404(Project.all_objects, id=project_id, is_deleted=True)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Proyecto eliminado permanentemente")
        return redirect('deleted_projects') 

    return redirect(reverse('deleted_projects'))

def deleted_projects(request):
    """
    Muestra una lista de proyectos eliminados.
    """
    client_profile = request.user.clientprofile
    deleted_projects = Project.all_objects.filter(client=client_profile, is_deleted=True)

    return render(request, 'Projects/deleted_projects.html', {
        'deleted_projects': deleted_projects,
    })

#@user_passes_test(is_client)
@login_required
def deleted_milestones(request, project_id):
    """
    Displays a list of deleted milestones.
    """
    project = get_object_or_404(Project.all_objects, id=project_id)
    client_profile = request.user.clientprofile
    deleted_milestones = Milestone.all_objects.filter(project__client=client_profile, is_deleted=True)

    return render(request, 'Projects/deleted_milestones.html', {
        'deleted_milestones': deleted_milestones,
        'project': project,	
    })

@login_required
def restore_milestone(request, milestone_id):
    """
    Restores a deleted milestone.
    """
    milestone = get_object_or_404(Milestone.all_objects, id=milestone_id, is_deleted=True)
    project = get_object_or_404(Project.all_objects, id=milestone.project.id)

    if request.method == "POST":
        milestone.is_deleted = False
        milestone.save()
        messages.success(request, ("Milestone restored successfully"))
        return redirect('deleted_milestones', project_id=project.id)

    return redirect('deleted_milestones', project_id=project.id)
  # O 'projects:deleted_milestones' si usas namespace

@login_required
def permanently_delete_milestone(request, milestone_id):
    """
    Permanently deletes a milestone.
    """
    milestone = get_object_or_404(Milestone.all_objects, id=milestone_id, is_deleted=True)
    project = get_object_or_404(Project.all_objects, id=milestone.project.id)
    if request.method == "POST":
        milestone.delete()
        messages.warning(request, ("Milestone permanently deleted"))
        return redirect('deleted_milestones', project_id=project.id) # O 'projects:deleted_milestones' si usas namespace

    return redirect('deleted_milestones', project_id=project.id)  # O 'projects:deleted_milestones' si usas namespace

# ----------------------------
# Vistas para Tareas
# ----------------------------

@login_required
def deleted_tasks(request, milestone_id):
    """
    Displays a list of deleted tasks.
    """
    milestone = get_object_or_404(Milestone.all_objects,id= milestone_id)
    client_profile = request.user.clientprofile
    deleted_tasks = Task.all_objects.filter(milestone__project__client=client_profile, is_deleted=True)

    return render(request, 'Projects/deleted_tasks.html', {
        'deleted_tasks': deleted_tasks,
        'milestone': milestone,
    })

@login_required
def restore_task(request, task_id):
    """
    Restores a deleted task.
    """
    task = get_object_or_404(Task.all_objects, id=task_id, is_deleted=True)
    milestone = get_object_or_404(Milestone.all_objects,id= task.milestone.id)

    if request.method == "POST":
        task.is_deleted = False
        task.save()
        messages.success(request, ("Task restored successfully"))
        return redirect('deleted_tasks',milestone_id=milestone.id)  # O 'projects:deleted_tasks' si usas namespace

    return redirect('deleted_tasks',milestone_id=milestone.id)  # O 'projects:deleted_tasks' si usas namespace

@login_required
def permanently_delete_task(request, task_id):
    """
    Permanently deletes a task.
    """
    task = get_object_or_404(Task.all_objects, id=task_id, is_deleted=True)
    milestone = get_object_or_404(Milestone.all_objects,id= task.milestone.id)

    if request.method == "POST":
        task.delete()
        messages.warning(request, ("Task permanently deleted"))
        return redirect('deleted_tasks',milestone_id=milestone.id)  # O 'projects:deleted_tasks' si usas namespace

    return redirect('deleted_tasks',milestone_id=milestone.id)

def redirect_to_client_payment_history(request):
    return redirect('client_payment_history')

def redirect_to_freelancer_payment_history(request):
    return redirect('freelancer_payment_history')