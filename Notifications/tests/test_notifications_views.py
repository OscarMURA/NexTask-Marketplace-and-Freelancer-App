# Notifications/tests/test_notifications_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from unittest.mock import patch, PropertyMock
from Notifications.models import Notification
from django.test.utils import override_settings

User = get_user_model()

class NotificationViewTests(TestCase):

    def setUp(self):
        # Crear un usuario y autenticarlo
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Crear notificaciones de ejemplo para el usuario
        self.unread_notification = Notification.objects.create(
            recipient=self.user, is_read=False, message="Unread Notification"
        )
        self.read_notification = Notification.objects.create(
            recipient=self.user, is_read=True, message="Read Notification"
        )

    def test_notification_list_view_authenticated(self):
        # Simular que el usuario es un freelancer
        with patch.object(type(self.user), 'is_freelancer', new_callable=PropertyMock, return_value=True):
            response = self.client.get(reverse('notification_list'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'notifications_list_freelancer.html')
            self.assertIn('notifications', response.context)
            self.assertIn('unread_notifications', response.context)
            self.assertIn(self.unread_notification, response.context['unread_notifications'])
            self.assertIn(self.read_notification, response.context['notifications'])

    def test_mark_all_as_read_action(self):
        # Probar marcar todas las notificaciones no leídas como leídas
        response = self.client.post(reverse('notification_list'), {'action': 'mark_all_as_read'})
        self.assertRedirects(response, reverse('notification_list'))
        self.unread_notification.refresh_from_db()
        self.assertTrue(self.unread_notification.is_read)

        # Verificar el mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Todas las notificaciones han sido marcadas como leídas.")

    def test_delete_read_notifications_action(self):
        # Probar eliminar todas las notificaciones leídas
        response = self.client.post(reverse('notification_list'), {'action': 'delete_read'})
        self.assertRedirects(response, reverse('notification_list'))
        self.assertFalse(Notification.objects.filter(id=self.read_notification.id).exists())

        # Verificar el mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Todas las notificaciones leídas han sido eliminadas.")

    def test_mark_single_notification_as_read_action(self):
        # Probar marcar una sola notificación como leída
        response = self.client.post(reverse('notification_list'), {
            'action': 'mark_as_read',
            'notification_id': self.unread_notification.id
        })
        self.assertRedirects(response, reverse('notification_list'))
        self.unread_notification.refresh_from_db()
        self.assertTrue(self.unread_notification.is_read)

        # Verificar el mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Notificación marcada como leída.")

    def test_delete_single_notification_action(self):
        # Probar eliminar una sola notificación
        response = self.client.post(reverse('notification_list'), {
            'action': 'delete',
            'notification_id': self.unread_notification.id
        })
        self.assertRedirects(response, reverse('notification_list'))
        self.assertFalse(Notification.objects.filter(id=self.unread_notification.id).exists())

        # Verificar el mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Notificación eliminada exitosamente.")

    def test_create_notification_view_get(self):
        # Reutilizar la lista de notificaciones para mostrar el formulario
        with patch.object(type(self.user), 'is_freelancer', new_callable=PropertyMock, return_value=False):
            response = self.client.get(reverse('create_notification'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'notifications_list_client.html')

    def test_create_notification_view_post(self):
        response = self.client.post(reverse('create_notification'), {
            'recipient': self.user.id,
            'message': 'New Notification'
        })
        self.assertRedirects(response, reverse('notification_list'))
        self.assertEqual(Notification.objects.count(), 3)  # 2 existentes + 1 nueva

    def test_notification_list_freelancer_view(self):
        # Simular que el usuario es un freelancer
        with patch.object(type(self.user), 'is_freelancer', new_callable=PropertyMock, return_value=True):
            response = self.client.get(reverse('notifications_list_freelancer'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'notifications_list_freelancer.html')
            self.assertIn('notifications', response.context)
            self.assertIn(self.unread_notification, response.context['notifications'])

    def test_notification_list_client_view(self):
        # Simular que el usuario es un cliente
        with patch.object(type(self.user), 'is_freelancer', new_callable=PropertyMock, return_value=False):
            response = self.client.get(reverse('notifications_list_client'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'notifications_list_client.html')
            self.assertIn('notifications', response.context)
            self.assertIn(self.unread_notification, response.context['notifications'])

    def test_mark_as_read_view(self):
        # Probar marcar una notificación como leída y eliminarla
        response = self.client.get(reverse('mark_as_read', args=[self.unread_notification.id]))
        self.assertRedirects(response, reverse('notification_list'))
        self.assertFalse(Notification.objects.filter(id=self.unread_notification.id).exists())

    def test_invalid_action_handling(self):
        # Probar el manejo de una acción no válida
        response = self.client.post(reverse('notification_list'), {'action': 'invalid_action'})
        self.assertRedirects(response, reverse('notification_list'))

        # Verificar que no se realizaron cambios en las notificaciones
        self.assertEqual(Notification.objects.filter(id=self.unread_notification.id).count(), 1)
        self.assertEqual(Notification.objects.filter(id=self.read_notification.id).count(), 1)

        # Verificar el mensaje de error apropiado
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("No se pudo procesar la notificación.", [str(message) for message in messages])