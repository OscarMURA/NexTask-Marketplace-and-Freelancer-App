from django.test import TestCase
from django.contrib.auth import get_user_model
from Notifications.models import Notification

User = get_user_model()

class NotificationModelTest(TestCase):
    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_create_notification(self):
        # Prueba la creación de una notificación
        notification = Notification.objects.create(
            recipient=self.user,
            message="Este es un mensaje de prueba"
        )

        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.message, "Este es un mensaje de prueba")
        self.assertFalse(notification.is_read)  
        self.assertIsNotNone(notification.created_at)

    def test_mark_notification_as_read(self):
        # Prueba marcar la notificación como leída
        notification = Notification.objects.create(
            recipient=self.user,
            message="Otra notificación de prueba"
        )

        self.assertFalse(notification.is_read)

        notification.is_read = True
        notification.save()

        updated_notification = Notification.objects.get(id=notification.id)
        self.assertTrue(updated_notification.is_read)

    def test_str_representation(self):
        # Prueba la representación en cadena
        notification = Notification.objects.create(
            recipient=self.user,
            message="Este es un mensaje de prueba",
            is_read=False,
        )
        expected_str_start = "Notification to testuser - Este es un mensaj"
        self.assertTrue(str(notification).startswith(expected_str_start))
