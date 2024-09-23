from django.shortcuts import render
from Projects.models import ProjectFreelancer, Task

def freelancer_report(request):
    freelancer = request.user.freelancer_profile
    project_associations = ProjectFreelancer.objects.filter(freelancer=freelancer)
    projects = [association.project for association in project_associations]
    
    total_projects = len(projects)
    total_milestones = sum([project.milestones.count() for project in projects])
    total_tasks = Task.objects.filter(assigned_to=freelancer).count()

    context = {
        'total_projects': total_projects,
        'total_milestones': total_milestones,
        'total_tasks': total_tasks,
        'projects': projects,
    }

    return render(request, 'reports/freelancer_report.html', context)


def client_report(request):
    client = request.user.client_profile
    projects = client.projects.all()

    total_projects = projects.count()
    projects_in_progress = projects.filter(actual_end_date__isnull=True).count()
    completed_projects = projects.filter(actual_end_date__isnull=False).count()

    total_tasks = {project: project.tasks.filter(status='completed').count() for project in projects}

    context = {
        'total_projects': total_projects,
        'projects_in_progress': projects_in_progress,
        'completed_projects': completed_projects,
        'total_tasks': total_tasks,
    }

    return render(request, 'reports/client_report.html', context)