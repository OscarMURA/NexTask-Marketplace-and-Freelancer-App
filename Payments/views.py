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
    
    payments = Payment.objects.filter(freelancer=freelancer_profile)
    
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
                status=Payment.PaymentStatus.PAID,
                client=client,
            )
            
            messages.success(request, _("Payment was successfully processed."))
            return HttpResponseRedirect(reverse("completed_payments"))
        
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

            return redirect('home_client')

        except ValueError:
            messages.error(request, _("Invalid input. Please check your entries."))
    
    return render(request, "Payments/periodic_payment.html", {
        "project": project,
        "freelancer": freelancer,
        "periodic_payment": periodic_payment
    })

@login_required
def pending_payments(request):
    """
    Muestra todos los pagos pendientes de un cliente o freelancer.
    """
    if request.user.user_type == 'client':
        # Filtrar los pagos pendientes para el cliente
        pending_payments = Payment.objects.filter(client__user=request.user, status='pending')
    elif request.user.user_type == 'freelancer':
        # Filtrar los pagos pendientes para el freelancer
        pending_payments = Payment.objects.filter(freelancer__user=request.user, status='pending')
    else:
        pending_payments = Payment.objects.none()  # Ningún pago si no es cliente o freelancer

    return render(request, 'payments/pending_payments.html', {
        'payments': pending_payments,
    })


@login_required
def completed_payments(request):
    """
    Muestra todos los pagos completados de un cliente o freelancer.
    """
    if request.user.user_type == 'client':
        # Filtrar los pagos completados para el cliente
        completed_payments = Payment.objects.filter(client__user=request.user, status='paid')
    elif request.user.user_type == 'freelancer':
        # Filtrar los pagos completados para el freelancer
        completed_payments = Payment.objects.filter(freelancer__user=request.user, status='paid')
    else:
        completed_payments = Payment.objects.none()

    return render(request, 'payments/completed_payments.html', {
        'payments': completed_payments,
    })

@login_required
def choose_payment_method(request, project_id, freelancer_id):
    """
    Permite al cliente escoger el método de pago y completa el pago si es seleccionado.
    """
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(FreelancerProfile, id=freelancer_id)
    client = get_object_or_404(ClientProfile, user=request.user)

    # Verificar si ya existe un pago pendiente
    payment = Payment.objects.filter(
        freelancer=freelancer,
        project=project,
        client=client,
        status=Payment.PaymentStatus.PENDING
    ).first()

    if request.method == "POST":
        method = request.POST.get("method")  # Método de pago seleccionado

        if payment:
            # Si ya existe un pago pendiente, completarlo
            payment.status = Payment.PaymentStatus.PAID
            payment.save()
            messages.success(request, "Pago completado exitosamente.")
        else:
            # Si no existe un pago pendiente, muestra un mensaje de error
            messages.error(request, "No hay pagos pendientes para este proyecto y freelancer.")
            return redirect('pending_payments')

        # Redirigir a la vista de recibo después del pago
        return redirect('payment_receipt', payment_id=payment.id)

    return render(request, 'payments/choose_payment_method.html', {
        'project': project,
        'freelancer': freelancer,
        'payment': payment
    })

@login_required
def payment_receipt(request, payment_id):
    """
    Muestra el recibo de un pago completado.
    """
    payment = get_object_or_404(Payment, id=payment_id)

    if payment.status == Payment.PaymentStatus.PENDING:
        messages.warning(request, "Este pago está pendiente. Completa el pago para ver el recibo.")
        return redirect('choose_payment_method', project_id=payment.project.id, freelancer_id=payment.freelancer.id)


    if request.user.user_type == 'freelancer':
        # Redirigir a la plantilla de recibo para freelancers
        template_name = 'payments/payment_receipt_freelancer.html'
    else:
        # Usar la plantilla de recibo para clientes
        template_name = 'payments/payment_receipt.html'

    return render(request, template_name, {
        'payment': payment,
    })


@login_required
def make_payment(request, payment_id):
    """
    Redirige a la selección del método de pago para el pago pendiente.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Redirigir a la selección del método de pago si el pago está pendiente
    if payment.status == Payment.PaymentStatus.PENDING:
        messages.info(request, "Por favor selecciona un método de pago.")
        return redirect('choose_payment_method', project_id=payment.project.id, freelancer_id=payment.freelancer.id)

    # Si el pago no está pendiente, redirige a la lista de pagos pendientes como fallback
    return redirect('pending_payments')