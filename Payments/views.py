from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from Users.models import FreelancerProfile, ClientProfile
from django.contrib import messages
from Projects.models import ProjectFreelancer, Project

@login_required
def client_payment_history(request):
    """
    Display the payment history for the client.
    Shows all payments associated with the projects created by the client.
    """
    client_profile = get_object_or_404(ClientProfile, user=request.user)
    
    # Obtener todos los proyectos del cliente a través de las asociaciones
    client_projects = ProjectFreelancer.objects.filter(project__client=client_profile)
    
    # Obtener todos los pagos relacionados con los proyectos del cliente
    payments = Payment.objects.filter(
        project__in=client_projects.values_list('project', flat=True)
    ).select_related('freelancer', 'project')
    
    return render(request, 'payments/client_payment_history.html', {'payments': payments})

@login_required
def freelancer_payment_history(request):
    """
    Display the payment history for the freelancer.
    Shows all payments associated with the freelancer.
    """
    freelancer_profile = get_object_or_404(FreelancerProfile, user=request.user)
    
    payments = Payment.objects.filter(freelancer=freelancer_profile).select_related('project')
    
    return render(request, 'payments/freelancer_payment_history.html', {'payments': payments})

@login_required
def freelancers_project_pay(request, project_id):
    """
    Displays a table of freelancers associated with a specific project.
    Allows the client to make payments to each freelancer in that project.
    """
    # Obtener el perfil del cliente
    client_profile = get_object_or_404(ClientProfile, user=request.user)
    
    # Obtener el proyecto actual por ID y verificar que sea del cliente
    project = get_object_or_404(Project, id=project_id, client=client_profile)

    # Obtener freelancers asociados al proyecto actual
    project_freelancers = ProjectFreelancer.objects.filter(project=project).select_related('freelancer')
    freelancers = [pf.freelancer for pf in project_freelancers]

    return render(request, 'payments/freelancers_project_pay.html', {'freelancers': freelancers, 'project': project})
