# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from Users.models import ClientProfile  # Asegúrate de importar ClientProfile
from .models import Project  



def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user.clientprofile  
            project.save()
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

    return render(request, 'Projects/homeClient.html', {'projects': projects})

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

