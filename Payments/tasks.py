from celery import shared_task
from django.utils import timezone
from Payments.models import PeriodicPayment

@shared_task
def check_periodic_payments():
    """
    Revisa todos los pagos periódicos y genera pagos pendientes si es necesario.
    """
    today = timezone.now().date()
    periodic_payments = PeriodicPayment.objects.filter(next_payment_date__lte=today)

    for periodic_payment in periodic_payments:
        # Genera un pago pendiente y actualiza la próxima fecha de pago
        periodic_payment.create_pending_payment()