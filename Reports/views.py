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
    reports = ReportLog.objects.filter(user=request.user).order_by('-created_at')  # Obtener informes generados anteriormente

    return {
        'reports': reports,  # Pasar los informes generados al template
    }

def client_report_view(request):
    context = get_client_report_context(request)
    return render(request, 'reports/client_report.html', context)

def view_report_detail(request, report_id):
    report = get_object_or_404(ReportLog, id=report_id, user=request.user)
    report_data = report.data or {}

    # Obtenemos todas las métricas presentes en report_data
    selected_metrics = report_data.keys()

    # Extrae los valores de las métricas
    progress = report_data.get("progress", 0)  # Valor predeterminado de 0 si no está definido
    remaining_progress = 100 - progress if progress is not None else 100
    budget_used = report_data.get("budget_used")
    milestones_count = report_data.get("milestones")
    completed_milestones = report_data.get("completed_milestones")
    incomplete_milestones = report_data.get("incomplete_milestones")
    completed_tasks_count = report_data.get("completed_tasks")
    incomplete_tasks_count = report_data.get("incomplete_tasks")

    context = {
        "report": report,
        "selected_metrics": selected_metrics,
        "progress": progress,
        "remaining_progress": remaining_progress,
        "budget_used": budget_used,
        "milestones_count": milestones_count,
        "completed_milestones": completed_milestones,
        "incomplete_milestones": incomplete_milestones,
        "completed_tasks_count": completed_tasks_count,
        "incomplete_tasks_count": incomplete_tasks_count,
    }

    return render(request, "reports/report_detail.html", context)
    
def get_generate_report_context(request):
    form = ReportFilterForm(request.GET or None)
    report_data = {}

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
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
            data=report_data
        )
        return {'report': report_log}

    return {'form': form}

def generate_report_view(request):
    form = ReportFilterForm(request.GET or None, user=request.user)
    report_data = {}
    selected_metrics = set()  # Para rastrear las métricas seleccionadas

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        metrics = form.cleaned_data['metrics']
        project_id = form.cleaned_data['project']

        project = Project.objects.get(id=project_id)

        # Cálculo del progreso
        if 'progress' in metrics:
            total_tasks = Task.objects.filter(milestone__project=project).count()
            completed_tasks = Task.objects.filter(milestone__project=project, status='completed').count()
            report_data['progress'] = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            selected_metrics.add('progress')  # Añadir a métricas seleccionadas

        # Cálculo del presupuesto utilizado
        if 'budget' in metrics:
            report_data['budget_used'] = float(project.budget)
            selected_metrics.add('budget')  # Añadir a métricas seleccionadas

        # Conteo de hitos
        if 'milestones' in metrics:
            milestones_count = project.milestones.count()
            report_data['milestones'] = milestones_count
            report_data['completed_milestones'] = project.milestones.filter(tasks__status='completed').distinct().count()
            report_data['incomplete_milestones'] = milestones_count - report_data['completed_milestones']
            selected_metrics.add('milestones')  # Añadir a métricas seleccionadas

        # Conteo de tareas completadas y sin completar
        if 'tasks' in metrics:
            report_data['completed_tasks'] = Task.objects.filter(milestone__project=project, status='completed').count()
            report_data['incomplete_tasks'] = Task.objects.filter(milestone__project=project).exclude(status='completed').count()
            selected_metrics.add('tasks')  # Añadir a métricas seleccionadas

        # Crear y almacenar el reporte
        report_log = ReportLog.objects.create(
            user=request.user,
            project=project,
            data=report_data
        )
        
        return render(request, 'reports/report_detail.html', {
            'report': report_log,
            'form': form,
            'selected_metrics': metrics,  # Para verificar qué métricas se seleccionaron
            'progress': report_data.get('progress'),  # Esto debería devolver el valor si existe
            'remaining_progress': 100 - report_data.get('progress', 0) if 'progress' in metrics else None,
            'budget_used': report_data.get('budget_used') if 'budget' in metrics else None,
            'milestones_count': report_data.get('milestones') if 'milestones' in metrics else None,
            'completed_milestones': report_data.get('completed_milestones') if 'milestones' in metrics else None,
            'incomplete_milestones': report_data.get('incomplete_milestones') if 'milestones' in metrics else None,
            'completed_tasks_count': report_data.get('completed_tasks') if 'tasks' in metrics else None,
            'incomplete_tasks_count': report_data.get('incomplete_tasks') if 'tasks' in metrics else None,
        })

    # Si el formulario no es válido
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
