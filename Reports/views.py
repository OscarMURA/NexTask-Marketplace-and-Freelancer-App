from django.shortcuts import render
from Projects.models import ProjectFreelancer, Task

def freelancer_report(request):
    """
    View to generate a report for the logged-in freelancer.

    This function gathers statistics about the freelancer's projects, milestones, and tasks.

    Context:
        total_projects (int): Total number of projects associated with the freelancer.
        total_milestones (int): Total number of milestones across all projects.
        total_tasks (int): Total number of tasks assigned to the freelancer.
        projects (list): List of projects associated with the freelancer.

    Returns:
        Rendered HTML response with the freelancer report.
    """
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
    """
    View to generate a report for the logged-in client.

    This function gathers statistics about the client's projects and tasks.

    Context:
        total_projects (int): Total number of projects associated with the client.
        projects_in_progress (int): Number of projects that are currently in progress (without actual end date).
        completed_projects (int): Number of projects that have been completed (with actual end date).
        total_tasks (dict): Dictionary with project as key and count of completed tasks as value.

    Returns:
        Rendered HTML response with the client report.
    """
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
