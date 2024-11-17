import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.test import Client
from Projects.models import Project
from Users.models import ClientProfile, FreelancerProfile, User
from Payments.models import Payment
from datetime import date
from django.test.utils import override_settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

@pytest.mark.django_db
class TestCreatePaymentView:

    def setup_method(self):
        # Crear cliente de prueba
        self.client = Client()
        # Crear usuario y perfiles asociados
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        self.client_profile = ClientProfile.objects.create(user=self.user)
        self.freelancer_user = User.objects.create_user(username='freelancer', email='freelancer@example.com', password='password')
        self.freelancer_profile = FreelancerProfile.objects.create(user=self.freelancer_user)

        # Crear un proyecto de prueba
        self.project = Project.objects.create(
            title="Test Project",
            budget=500.00,
            client=self.client_profile,
            description='{"delta": {}, "html": "<p>Test description</p>"}',
            start_date=date.today(),
            due_date=date.today()
        )

        # Asociar freelancer al proyecto
        self.project.freelancer_associations.create(freelancer=self.freelancer_profile)

        # Iniciar sesión con el cliente de prueba
        self.client.login(username='testuser', password='password')

    @patch('mercadopago.SDK.preference')
    def test_create_payment_successful(self, mock_preference):
        # Configurar respuesta simulada
        mock_response = MagicMock()
        mock_response.create.return_value = {
            "response": {
                "init_point": "https://www.mercadopago.com/init_point"
            }
        }
        mock_preference.return_value = mock_response

        with override_settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
            response = self.client.get(reverse('create_payment', args=[self.project.id]))

        # Verificar redirección
        assert response.status_code == 302
        assert response.url == "https://www.mercadopago.com/init_point"

        # Verificar que el pago se haya creado con estado 'pending'
        payment = Payment.objects.get(project=self.project)
        assert payment.status == "pending"
        assert payment.amount == self.project.budget

    @patch('mercadopago.SDK.preference')
    def test_create_payment_handles_mercadopago_error(self, mock_preference):
        # Simular error en MercadoPago
        mock_preference.side_effect = Exception("MercadoPago Error")

        with override_settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
            with pytest.raises(Exception, match="MercadoPago Error"):
                self.client.get(reverse('create_payment', args=[self.project.id]))

    def test_create_payment_project_not_found(self):
        with override_settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
            with pytest.raises(ObjectDoesNotExist):
                self.client.get(reverse('create_payment', args=[999]))  # ID no existente

    def test_client_payment_history_view(self):
        # Verifica que la vista de historial del cliente funcione
        with override_settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
            response = self.client.get(reverse('client_payment_history'))
            assert response.status_code == 200
            assert isinstance(response, HttpResponse)
            assert response.content == b"Client payment history placeholder."

    def test_freelancer_payment_history_view(self):
        # Verifica que la vista de historial del freelancer funcione
        with override_settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
            response = self.client.get(reverse('freelancer_payment_history'))
            assert response.status_code == 200
            assert isinstance(response, HttpResponse)
            assert response.content == b"Freelancer payment history placeholder."
