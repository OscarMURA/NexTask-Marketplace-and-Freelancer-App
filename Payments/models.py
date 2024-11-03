from django.db import models
from django.utils.translation import gettext_lazy as _
from Users.models import FreelancerProfile  # Importa el modelo de FreelancerProfile
from Projects.models import Project  # Importa el modelo de Project

class Payment(models.Model):
    """
    Represents a one-time payment associated with a project and a freelancer.
    
    Attributes:
        freelancer (FreelancerProfile): ForeignKey to the FreelancerProfile model.
        project (Project): ForeignKey to the Project model.
        amount (Decimal): The amount to be paid.
        status (str): The status of the payment (pending or paid).
    """
    
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')

    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='payments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Define el monto del pago
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    client = models.ForeignKey('Users.ClientProfile', on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"Payment of {self.amount} for {self.freelancer.user.username} - Status: {self.status}"