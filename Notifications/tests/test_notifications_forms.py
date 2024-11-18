from django.test import TestCase
from Notifications.forms import NotificationForm  
from Notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationFormTest(TestCase):
    def setUp(self):
        # Crea un usuario de prueba para usar como destinatario
        self.recipient = User.objects.create_user(username='recipientuser', password='recipientpassword')

    def test_notification_form_valid_data(self):
        # Prueba con datos válidos para el formulario
        form = NotificationForm(data={
            'recipient': self.recipient.id,
            'message': 'This is a test notification.'
        })
        self.assertTrue(form.is_valid())

    def test_notification_form_empty_data(self):
        # Prueba con datos vacíos, el formulario no debe ser válido
        form = NotificationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('recipient', form.errors)
        self.assertIn('message', form.errors)

    def test_notification_form_missing_recipient(self):
        # Prueba sin el campo 'recipient', el formulario no debe ser válido
        form = NotificationForm(data={'message': 'This is a test notification.'})
        self.assertFalse(form.is_valid())
        self.assertIn('recipient', form.errors)

    def test_notification_form_missing_message(self):
        # Prueba sin el campo 'message', el formulario no debe ser válido
        form = NotificationForm(data={'recipient': self.recipient.id})
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
