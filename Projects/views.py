# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from Users.models import ClientProfile  # Asegúrate de importar ClientProfile

from .models import *
from django.urls import reverse
from django.contrib import messages
from .models import Project, Milestone,Task
from .forms import MilestoneForm, TaskForm
from django.db.models import Q
from Users.models import FreelancerProfile, Skill, Language

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user.clientprofile  
            project.save()
            print(project.category)
            print("Proyecto creado", project)  # Imprimir el proyecto creado
            return redirect('home_client')  # Redirigir a la lista de proyectos o a una página de éxito
        else:
            print("Error en el formulario", form.errors)
    else:
        form = ProjectForm()
        

    return render(request, 'Projects/createProject.html', {'form': form})

def home_client(request):
    # Supongamos que el cliente está autenticado y puedes acceder a su perfil
    client_profile = request.user.clientprofile  # Asumiendo que el usuario tiene un perfil de cliente
    projects = client_profile.projects.all()  # Obtiene todos los proyectos asociados al cliente
    total_projects = projects.count()  # Número total de proyectos
    total_balance = client_profile.get_total_budget()  # Presupuesto total

    return render(request, 'Projects/homeClient.html', {
        'projects': projects,
        'total_projects': total_projects,
        'total_balance': total_balance,
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'Projects/project_detail.html', {'project': project})

def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)  # Redirige a la página de detalles del proyecto
    else:
        form = ProjectForm(instance=project)
        
    return render(request, 'Projects/edit_project.html', {'form': form, 'project': project})

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Proyecto eliminado exitosamente")
        return redirect('home_client') 

    return redirect(reverse('home_client'))

# Crear un nuevo hito para un proyecto específico
def create_milestone(request, project_id):
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

# Editar un hito existente
def edit_milestone(request, milestone_id):
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
    milestone = get_object_or_404(Milestone, pk=pk)
    return render(request, 'Projects/milestone_detail.html', {'milestone': milestone})

def delete_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)
    project_id = milestone.project.id

    if request.method == "POST":
        milestone.delete()
        messages.success(request, "Milestone eliminado exitosamente")
        return redirect('project_detail', project_id=project_id)

    return redirect(reverse('home_client'))


# Vista para crear una nueva tarea
def create_task(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.milestone = milestone  # Asociar la tarea con el hito
            task.save()
            return redirect('milestone_detail', pk=milestone.id)
    else:
        form = TaskForm()

    # Pasar el hito al contexto
    return render(request, 'Projects/create_task.html', {'form': form, 'milestone': milestone})


# Vista para editar una tarea existente
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('milestone_detail', pk=task.milestone.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'Projects/edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    milestone_id = task.milestone.id

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('milestone_detail', pk=milestone_id)

    return redirect('milestone_detail', pk=milestone_id)


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'Projects/task_detail.html', {'task': task})

def search_freelancer(request, project_id):
    # Obtener el proyecto a través del project_id
    project = get_object_or_404(Project, id=project_id)

    freelancers = FreelancerProfile.objects.all()
    skills = Skill.objects.all()
    languages = Language.objects.all()
    countries = FreelancerProfile.objects.values_list('country', flat=True).distinct()

    # Filtrar por los parámetros de búsqueda
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
        'project': project,  # Asegúrate de pasar el proyecto al contexto
        'freelancers': freelancers,
        'skills': skills,
        'languages': languages,
        'countries': countries,
    }

    return render(request, 'Projects/search_freelancer.html', context)



def freelancer_profile(request, project_id, freelancer_id):
    # Obtener el proyecto y el freelancer
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, user__id=freelancer_id)

    context = {
        'project': project,
        'freelancer': freelancer,
    }

    return render(request, 'Projects/freelancer_profile.html', context)


def create_project_freelancer_association(request, project_id, freelancer_id):
    # Obtener el proyecto
    project = get_object_or_404(Project, id=project_id)
    
    # Verificar si el FreelancerProfile está asociado al user con el freelancer_id
    freelancer = get_object_or_404(FreelancerProfile, user__id=freelancer_id)

    # Crear la asociación entre el proyecto y el freelancer
    association, created = ProjectFreelancer.objects.get_or_create(
        project=project,
        freelancer=freelancer,
        defaults={'status': 'pending'}
    )
    
    if created:
        messages.success(request, f"Contract pending for {freelancer.user.username} on project {project.title}")
    else:
        messages.info(request, f"A contract already exists for {freelancer.user.username} on project {project.title}")

    # Redirigir a la vista de detalles del proyecto
    return redirect('project_detail', project_id=project.id)


def manage_applications(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    applications = Application.objects.filter(project=project)

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        # Obtener la aplicación correspondiente
        application = get_object_or_404(Application, id=application_id)

        if action == 'accept':
            # Crear el contrato
            Contract.objects.create(
                project=application.project,
                freelancer=application.freelancer
            )
            # Eliminar la aplicación después de aceptar
            application.delete()
            messages.success(request, f"Freelancer {application.freelancer.user.username} accepted and contract created.")
            return redirect('home_client')

        elif action == 'reject':
            # Eliminar la aplicación cuando se rechace
            application.delete()
            messages.info(request, f"Freelancer {application.freelancer.user.username} rejected.")
            return redirect('home_client')

    return render(request, 'projects/manageApplications.html', {
        'project': project,
        'applications': applications,
    })



@login_required
def search_projects(request):
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
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'Projects/view_project_search_freelancer_dashboard.html', {'project': project})

@login_required
def apply_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not hasattr(request.user, 'freelancer_profile'):
        return redirect('register_freelancer')

    application, created = Application.objects.get_or_create(
        freelancer=request.user.freelancer_profile, project=project
    )

    return redirect('application_confirmation')

def application_confirmation(request):
    return render(request, 'Projects/application_confirmation.html')

@login_required
def search_public_projects(request):
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
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'Projects/view_project_search.html', {'project': project})

def freelancer_profile_manage(request, project_id, freelancer_id):
    # Obtener el proyecto y el freelancer
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, user__id=freelancer_id)

    context = {
        'project': project,
        'freelancer': freelancer,
    }

    return render(request, 'Projects/freelancer_profile_manage.html', context)