from django.shortcuts import render, get_object_or_404 
from Projects.models import ProjectFreelancer, Task, Project
from .models import ReportLog
from .forms import ReportFilterForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string


def get_client_report_context(request):
    client = request.user.clientprofile
    projects = client.projects.all()

    total_projects = projects.count()
    projects_in_progress = projects.filter(actual_end_date__isnull=True).count()
    completed_projects = projects.filter(actual_end_date__isnull=False).count()

    form = ReportFilterForm(request.GET or None)
    filtered_data = {}
    
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        for project in projects:
            tasks = project.tasks.filter(status='completed')
            if start_date:
                tasks = tasks.filter(due_date__gte=start_date)
            if end_date:
                tasks = tasks.filter(due_date__lte=end_date)
            filtered_data[project] = tasks.count()

        metrics = form.cleaned_data.get('metrics')
        if metrics:
            if 'progress' in metrics:
                filtered_data['progress'] = sum(project.get_progress() for project in projects) / total_projects
            if 'milestones' in metrics:
                filtered_data['milestones'] = sum(project.milestones.count() for project in projects)
            if 'tasks' in metrics:
                filtered_data['tasks'] = {project: filtered_data.get(project, 0) for project in projects}

    return {
        'form': form,
        'total_projects': total_projects,
        'projects_in_progress': projects_in_progress,
        'completed_projects': completed_projects,
        **filtered_data,
    }

def client_report_view(request):
    context = get_client_report_context(request)
    return render(request, 'reports/client_report.html', context)

def get_generate_report_context(request):
    form = ReportFilterForm(request.GET or None)
    report_data = {}

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        report_type = form.cleaned_data.get('report_type')
        metrics = form.cleaned_data.get('metrics')
        project = form.cleaned_data.get('project')

        if project:
            report_data['project'] = project.title
            if 'progress' in metrics:
                report_data['progress'] = project.get_progress()
            if 'milestones' in metrics:
                report_data['milestones'] = project.milestones.count()
            if 'tasks' in metrics:
                tasks = project.tasks.all()
                if start_date:
                    tasks = tasks.filter(due_date__gte=start_date)
                if end_date:
                    tasks = tasks.filter(due_date__lte=end_date)
                report_data['total_tasks'] = tasks.count()

        report_log = ReportLog.objects.create(
            user=request.user,
            project=project,
            report_type=report_type,
            data=report_data
        )
        return {'report': report_log}

    return {'form': form}

def generate_report_view(request):
    form = ReportFilterForm(request.GET or None, user=request.user)
    report_data = {}

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        report_type = form.cleaned_data['report_type']
        metrics = form.cleaned_data['metrics']
        project_id = form.cleaned_data['project']

        project = Project.objects.get(id=project_id)

        # Cálculo del progreso
        if 'progress' in metrics:
            total_tasks = Task.objects.filter(milestone__project=project).count()
            completed_tasks = Task.objects.filter(milestone__project=project, status='completed').count()
            report_data['progress'] = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            print("Progress Calculated:", report_data['progress'])  # Debug

        # Cálculo del presupuesto utilizado
        if 'budget' in metrics:
            report_data['budget_used'] = float(project.budget)  # Convertir Decimal a float
            print("Budget Used:", report_data['budget_used'])  # Debug

        # Conteo de hitos
        if 'milestones' in metrics:
            milestones_count = project.milestones.count()
            report_data['milestones'] = milestones_count
            print("Milestones Count:", report_data['milestones'])  # Debug
            
            # Hitos completados
            completed_milestones = project.milestones.filter(tasks__status='completed').distinct().count()
            report_data['completed_milestones'] = completed_milestones
            print("Completed Milestones:", report_data['completed_milestones'])  # Debug
            
            # Hitos sin completar
            incomplete_milestones = milestones_count - completed_milestones
            report_data['incomplete_milestones'] = incomplete_milestones
            print("Incomplete Milestones:", report_data['incomplete_milestones'])  # Debug

        # Conteo de tareas completadas y sin completar
        if 'tasks' in metrics:
            completed_tasks_count = Task.objects.filter(milestone__project=project, status='completed').count()
            report_data['completed_tasks'] = completed_tasks_count
            print("Completed Tasks:", report_data['completed_tasks'])  # Debug
            
            # Tareas sin completar
            incomplete_tasks_count = Task.objects.filter(milestone__project=project).exclude(status='completed').count()
            report_data['incomplete_tasks'] = incomplete_tasks_count
            print("Incomplete Tasks:", report_data['incomplete_tasks'])  # Debug

        # Almacenar el registro en el reporte
        report_log = ReportLog.objects.create(
            user=request.user,
            project=project,
            report_type=report_type,
            data=report_data
        )

        # Verificar el contenido antes de renderizar
        print("Final Report Data:", report_data)  # Debug
        
        return render(request, 'reports/report_detail.html', {
            'report': report_log,
            'form': form,
            'progress': report_data.get('progress', 0),
            'remaining_progress': 100 - report_data.get('progress', 0),
            'milestones_count': report_data.get('milestones', 0),
            'completed_milestones': report_data.get('completed_milestones', 0),
            'incomplete_milestones': report_data.get('incomplete_milestones', 0),
            'completed_tasks_count': report_data.get('completed_tasks', 0),
            'incomplete_tasks_count': report_data.get('incomplete_tasks', 0),
            'budget_used': report_data.get('budget_used', 0)
        })
    
    # Si el formulario no es válido, mostramos los errores
    print("Form Errors:", form.errors)  # Debug
    return render(request, 'reports/generate_report.html', {'form': form})
    
def project_report(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = ReportFilterForm(request.GET or None)
    report_data = {
        'project_title': project.title,
        'total_milestones': project.milestones.count(),
        'total_tasks': project.tasks.count(),
    }

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        metrics = form.cleaned_data.get('metrics')

        if metrics:
            if 'progress' in metrics:
                report_data['progress'] = project.get_progress()
            if 'milestones' in metrics:
                milestones = project.milestones.all()
                if start_date:
                    milestones = milestones.filter(due_date__gte=start_date)
                if end_date:
                    milestones = milestones.filter(due_date__lte=end_date)
                report_data['filtered_milestones'] = milestones.count()
            if 'tasks' in metrics:
                tasks = project.tasks.all()
                if start_date:
                    tasks = tasks.filter(due_date__gte=start_date)
                if end_date:
                    tasks = tasks.filter(due_date__lte=end_date)
                report_data['filtered_tasks'] = tasks.count()

    return render(request, 'reports/project_report.html', {
        'form': form,
        'report_data': report_data,
        'project': project
    })
