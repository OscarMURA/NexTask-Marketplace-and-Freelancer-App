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
    total_reports = reports.count()  # Cuenta los reportes generados por el usuario


    return {
        'reports': reports,  # Pasar los informes generados al template
        'total_reports': total_reports,  # Total de reportes para mostrar en el dashboard
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
    milestones_data = report_data.get("milestones", [])  # Asegúrate de extraer la información de los hitos
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
        "milestones_data": milestones_data,  # Incluye los datos de los hitos en el contexto
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

        # Cálculo del progreso del proyecto
        if 'progress' in metrics:
            total_tasks = Task.objects.filter(milestone__project=project).count()
            completed_tasks = Task.objects.filter(milestone__project=project, status='completed').count()
            report_data['progress'] = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            selected_metrics.add('progress')

        # Cálculo del presupuesto utilizado
        if 'budget' in metrics:
            report_data['budget_used'] = float(project.budget)
            selected_metrics.add('budget')

        # Detalle de los hitos
        if 'milestones' in metrics:
            completed_milestones = 0
            incomplete_milestones = 0
            milestones_data = []

            for milestone in project.milestones.all():
                milestone_tasks = milestone.tasks.all()
                total_tasks = milestone_tasks.count()
                completed_tasks = milestone_tasks.filter(status='completed').count()

                # Determinar si el hito está completo
                if total_tasks > 0 and total_tasks == completed_tasks:
                    completed_milestones += 1
                else:
                    incomplete_milestones += 1

                # Progreso del hito
                progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

                # Obtener los freelancers asignados para cada tarea
                tasks_data = []
                for task in milestone_tasks:
                    freelancers = []
                    if task.assigned_to:
                        freelancers.append(task.assigned_to.user.get_full_name())  # Obtener nombre completo

                    tasks_data.append({
                        'title': task.title,
                        'status': task.status.replace('_', ' ').title(),
                        'priority': task.priority.replace('_', ' ').title(),
                        'freelancers': freelancers
                    })

                milestones_data.append({
                    'title': milestone.title,
                    'start_date': milestone.start_date.strftime('%Y-%m-%d') if milestone.start_date else None,
                    'due_date': milestone.due_date.strftime('%Y-%m-%d') if milestone.due_date else None,
                    'progress': progress,
                    'tasks': tasks_data
                })

            report_data['milestones'] = milestones_data
            report_data['completed_milestones'] = completed_milestones
            report_data['incomplete_milestones'] = incomplete_milestones
            selected_metrics.add('milestones')

        # Conteo de tareas
        if 'tasks' in metrics:
            report_data['completed_tasks'] = Task.objects.filter(milestone__project=project, status='completed').count()
            report_data['incomplete_tasks'] = Task.objects.filter(milestone__project=project).exclude(status='completed').count()
            selected_metrics.add('tasks')

        # Crear y almacenar el reporte
        report_log = ReportLog.objects.create(
            user=request.user,
            project=project,
            data=report_data
        )

        return render(request, 'reports/report_detail.html', {
            'report': report_log,
            'form': form,
            'selected_metrics': metrics,
            'progress': report_data.get('progress'),
            'remaining_progress': 100 - report_data.get('progress', 0) if 'progress' in metrics else None,
            'budget_used': report_data.get('budget_used') if 'budget' in metrics else None,
            'milestones_data': report_data.get('milestones') if 'milestones' in metrics else None,
            'completed_milestones': report_data.get('completed_milestones') if 'milestones' in metrics else 0,
            'incomplete_milestones': report_data.get('incomplete_milestones') if 'milestones' in metrics else 0,
            'completed_tasks_count': report_data.get('completed_tasks') if 'tasks' in metrics else None,
            'incomplete_tasks_count': report_data.get('incomplete_tasks') if 'tasks' in metrics else None,
        })

    # Si el formulario no es válido
    return render(request, 'reports/generate_report.html', {'form': form})
