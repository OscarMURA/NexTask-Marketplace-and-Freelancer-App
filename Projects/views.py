# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from Users.models import ClientProfile  # Asegúrate de importar ClientProfile
from .models import Project  
from django.urls import reverse
from django.contrib import messages
from .models import Project, Milestone
from .forms import MilestoneForm
from django.core.paginator import Paginator
from .models import Project, Milestone,Task
from .forms import MilestoneForm, TaskForm

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
    client_profile = request.user.clientprofile  # Asumiendo que el usuario tiene un perfil de cliente

    # Obtiene todos los proyectos asociados al cliente y los ordena
    projects = client_profile.projects.all().order_by('-created_at')
    
    # Paginación
    paginator = Paginator(projects, 5)  # 10 proyectos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Solo se necesita pasar 'page_obj' para la paginación junto con cualquier otra variable necesaria
    return render(request, 'Projects/homeClient.html', {
        'page_obj': page_obj,
        'total_projects': projects.count(),  # Número total de proyectos
        'total_balance': client_profile.get_total_budget()  # Presupuesto total
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

