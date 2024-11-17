from django.db import models
from django.utils.translation import gettext_lazy as _
from Users.models import FreelancerProfile, ClientProfile
from Projects.models import Project
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment of {self.amount} for {self.freelancer.user.username} - Status: {self.status}"
    
class PeriodicPayment(models.Model):
    """
    Configuración para pagos periódicos entre un cliente y un freelancer en un proyecto.
    """
    class Frequency(models.TextChoices):
        DAILY = 'daily', _('Daily')
        WEEKLY = 'weekly', _('Weekly')
        MONTHLY = 'monthly', _('Monthly')

    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='periodic_payments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='periodic_payments')
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='periodic_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto por cada periodo
    frequency = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.WEEKLY)
    start_date = models.DateField()  # Fecha de inicio del pago periódico
    end_date = models.DateField(null=True, blank=True)  # Fecha opcional de fin del pago periódico
    next_payment_date = models.DateField()  # Fecha del próximo pago programado

    def __str__(self):
        return f"{self.freelancer.user.username} - {self.project.title} ({self.frequency})"
    
    def generate_next_payment_date(self):
        """
        Genera la próxima fecha de pago de acuerdo con la frecuencia establecida.
        """
        if self.frequency == self.Frequency.DAILY:
            return self.next_payment_date + timedelta(days=1)
        elif self.frequency == self.Frequency.WEEKLY:
            return self.next_payment_date + timedelta(weeks=1)
        elif self.frequency == self.Frequency.MONTHLY:
            return self.next_payment_date + timedelta(days=30)  # Aproximado para meses

    def create_pending_payment(self):
        """
        Crea un registro de pago puntual pendiente cuando llega la fecha de pago.
        """
        from Payments.models import Payment  # Importar modelo de Payment para evitar importaciones circulares
        
        if self.next_payment_date <= timezone.now().date():
            Payment.objects.create(
                freelancer=self.freelancer,
                project=self.project,
                amount=self.amount,
                status=Payment.PaymentStatus.PENDING,
                client=self.client
            )
            self.next_payment_date = self.generate_next_payment_date()  # Actualiza la próxima fecha de pago
            self.save()

    def clean(self):
        """
        Valida que solo exista un pago periódico para cada freelancer y proyecto.
        """
        if PeriodicPayment.objects.filter(freelancer=self.freelancer, project=self.project).exists():
            raise ValidationError(_('There is already a periodic payment for this freelancer on this project.'))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['freelancer', 'project'], name='unique_periodic_payment_per_project')
        ]