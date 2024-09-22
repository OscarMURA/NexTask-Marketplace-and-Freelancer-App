from django.shortcuts import render

import mercadopago
from django.conf import settings
from django.shortcuts import redirect
from Projects.models import Project
from Users.models import ClientProfile, FreelancerProfile
from .models import Payment

def create_payment(request, project_id):
    project = Project.objects.get(id=project_id)
    freelancer = project.freelancer_associations.first().freelancer
    amount = project.budget
    
    # Configuración del cliente de MercadoPago
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    preference_data = {
        "items": [
            {
                "title": f"Payment for project {project.title}",
                "quantity": 1,
                "unit_price": float(amount),
            }
        ],
        "payer": {
            "email": request.user.email,
        },
        "back_urls": {
            "success": "https://tu-plataforma.com/success/",
            "failure": "https://tu-plataforma.com/failure/",
            "pending": "https://tu-plataforma.com/pending/",
        },
        "auto_return": "approved",
    }

    # Crear la preferencia de pago
    preference = sdk.preference().create(preference_data)
    Payment.objects.create(project=project, client=project.client, freelancer=freelancer, amount=amount, status="pending")

    return redirect(preference["response"]["init_point"])

