from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment, PeriodicPayment
from Users.models import FreelancerProfile, ClientProfile
from django.contrib import messages
from Projects.models import ProjectFreelancer, Project, Contract
from Notifications.models import Notification
from django.utils.translation import gettext_lazy as _
import time

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

    # Obtener contratos asociados al proyecto actual
    freelancers = Contract.objects.filter(project=project)

    return render(request, 'payments/freelancers_project_pay.html', {
        'freelancers': freelancers,
        'project': project,
    })

@login_required
def freelancers_project_punctual_pay(request, project_id, freelancer_id):
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, id=freelancer_id)
    client = get_object_or_404(ClientProfile, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError(_("Amount must be positive."))
            
            # Crear el pago puntual
            Payment.objects.create(
                freelancer=freelancer,
                project=project,
                amount=amount,
                status=Payment.PaymentStatus.PENDING,
                client=client,
            )
            
            messages.success(request, _("Payment was successfully processed."))
            return HttpResponseRedirect(reverse("client_payment_history"))
        
        except (ValueError, TypeError):
            messages.error(request, _("Invalid amount. Please enter a valid number."))
            return render(request, "Payments/punctual_payment.html", {"project": project, "freelancer": freelancer})
    
    return render(request, "Payments/punctual_payment.html", {"project": project, "freelancer": freelancer})

@login_required
def freelancers_project_periodic_pay(request, project_id, freelancer_id):
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, id=freelancer_id)
    client = get_object_or_404(ClientProfile, user=request.user)

    # Intenta cargar un pago periódico existente para el freelancer y el proyecto
    periodic_payment = PeriodicPayment.objects.filter(freelancer=freelancer, project=project).first()
    print(periodic_payment)

    if request.method == "POST":
        amount = request.POST.get("amount")
        frequency = request.POST.get("frequency")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date") or None

        try:
            amount = float(amount)
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None

            if periodic_payment:
                # Si existe, actualizar el pago periódico existente
                periodic_payment.amount = amount
                periodic_payment.frequency = frequency
                periodic_payment.start_date = start_date
                periodic_payment.end_date = end_date
                periodic_payment.next_payment_date = start_date
                periodic_payment.save()
                messages.success(request, _("Periodic payment updated successfully."))
            else:
                # Si no existe, crear un nuevo pago periódico
                PeriodicPayment.objects.create(
                    freelancer=freelancer,
                    project=project,
                    client=client,
                    amount=amount,
                    frequency=frequency,
                    start_date=start_date,
                    end_date=end_date,
                    next_payment_date=start_date
                )
                messages.success(request, _("Periodic payment setup was successful."))

            return redirect('client_payment_history')

        except ValueError:
            messages.error(request, _("Invalid input. Please check your entries."))
    
    return render(request, "Payments/periodic_payment.html", {
        "project": project,
        "freelancer": freelancer,
        "periodic_payment": periodic_payment
    })

@login_required
def payment_history(request):
    # Filtra los pagos de acuerdo al tipo de usuario
    if request.user.user_type == 'client':
        payments = Payment.objects.filter(client__user=request.user).order_by('-created_at')
    elif request.user.user_type == 'freelancer':
        payments = Payment.objects.filter(freelancer__user=request.user).order_by('-created_at')
    else:
        payments = Payment.objects.none()  # Ningún pago si no es cliente o freelancer

    # Renderiza la plantilla con el historial de pagos
    return render(request, 'Payments/payment_history.html', {'payments': payments})
