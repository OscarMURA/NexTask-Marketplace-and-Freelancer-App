# views.py
from django.shortcuts import render, redirect
from .forms import ProjectForm
from Users.models import ClientProfile  # Asegúrate de importar ClientProfile
from .models import Project  # Asegúrate de que Project esté importado



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
    return render(request, 'Projects/homeClient.html')
