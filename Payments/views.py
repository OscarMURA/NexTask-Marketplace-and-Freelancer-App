from django.shortcuts import render
import mercadopago
from django.conf import settings
from django.shortcuts import redirect
from Projects.models import Project
from Users.models import ClientProfile, FreelancerProfile
from .models import Payment

def create_payment(request, project_id):
    """
    Creates a payment preference using MercadoPago for a specified project.

    Args:
        request (HttpRequest): The HTTP request object.
        project_id (int): The ID of the project for which the payment is being made.

    Returns:
        HttpResponse: Redirects to the MercadoPago payment page.
    """
    
    # Retrieve the project by its ID
    project = Project.objects.get(id=project_id)
    # Get the associated freelancer for the project
    freelancer = project.freelancer_associations.first().freelancer
    # Get the project budget for the payment amount
    amount = project.budget
    
    # Configure the MercadoPago client with the access token from settings
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    # Prepare the payment preference data
    preference_data = {
        "items": [
            {
                "title": f"Payment for project {project.title}",
                "quantity": 1,
                "unit_price": float(amount),  # Convert amount to float for MercadoPago
            }
        ],
        "payer": {
            "email": request.user.email,  # Get the email of the authenticated user
        },
        "back_urls": {
            "success": "https://tu-plataforma.com/success/",  # URL to redirect on successful payment
            "failure": "https://tu-plataforma.com/failure/",  # URL to redirect on payment failure
            "pending": "https://tu-plataforma.com/pending/",  # URL for pending payments
        },
        "auto_return": "approved",  # Automatically return to the specified URL on approval
    }

    # Create the payment preference in MercadoPago
    preference = sdk.preference().create(preference_data)
    # Log the payment information in the database with status as pending
    Payment.objects.create(project=project, client=project.client, freelancer=freelancer, amount=amount, status="pending")

    # Redirect the user to the payment initiation point
    return redirect(preference["response"]["init_point"])
