import pytest
from decimal import Decimal
from Projects.models import Project
from Users.models import ClientProfile, FreelancerProfile, User
from Payments.models import Payment
from datetime import date

@pytest.mark.django_db
class TestPaymentModel:

    def setup_method(self):
        # Crear datos de usuario, cliente y freelancer
        self.user_client = User.objects.create_user(username='clientuser', email='client@example.com', password='password')
        self.client_profile = ClientProfile.objects.create(user=self.user_client)

        self.user_freelancer = User.objects.create_user(username='freelanceruser', email='freelancer@example.com', password='password')
        self.freelancer_profile = FreelancerProfile.objects.create(user=self.user_freelancer)

        # Crear un proyecto de prueba
        self.project = Project.objects.create(
            title="Test Project",
            budget=500.00,
            client=self.client_profile,
            description='{"delta": {}, "html": "<p>Test project description</p>"}',
            start_date=date.today(),
            due_date=date.today()
        )

    def test_payment_creation(self):
        # Crear una instancia de Payment
        payment = Payment.objects.create(
            project=self.project,
            client=self.client_profile,
            freelancer=self.freelancer_profile,
            amount=Decimal('500.00'),
            status='pending'
        )

        # Verificar que el pago se haya creado correctamente
        assert payment.project == self.project
        assert payment.client == self.client_profile
        assert payment.freelancer == self.freelancer_profile
        assert payment.amount == Decimal('500.00')
        assert payment.status == 'pending'
        assert payment.created_at is not None

    def test_payment_str_representation(self):
        # Crear una instancia de Payment
        payment = Payment.objects.create(
            project=self.project,
            client=self.client_profile,
            freelancer=self.freelancer_profile,
            amount=Decimal('750.00'),
            status='completed'
        )

        # Verificar la representación en string
        assert str(payment) == f"Payment for {self.project.title} - 750.00 USD"

    def test_payment_status_choices(self):
        # Verificar que solo se puedan asignar valores válidos a 'status'
        payment = Payment.objects.create(
            project=self.project,
            client=self.client_profile,
            freelancer=self.freelancer_profile,
            amount=Decimal('300.00'),
            status='pending'
        )

        assert payment.status in dict(Payment.STATUS_CHOICES)

        # Cambiar el estado a 'completed'
        payment.status = 'completed'
        payment.save()
        assert payment.status == 'completed'

        # Cambiar el estado a 'failed'
        payment.status = 'failed'
        payment.save()
        assert payment.status == 'failed'
