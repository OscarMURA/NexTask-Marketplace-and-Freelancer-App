from django.test import TestCase
from django.contrib.auth import get_user_model
from Reports.models import ReportLog
from datetime import datetime
from django.utils.timezone import now

User = get_user_model()

class ReportLogModelTest(TestCase):

    def setUp(self):
        # Crear un usuario para los registros de reporte
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_crear_report_log(self):
        """
        Prueba que se pueda crear un registro de ReportLog correctamente.
        """
        report_log = ReportLog.objects.create(user=self.user, report_type='mensual')
        
        # Verificar que el objeto se creó correctamente
        self.assertEqual(report_log.user, self.user)
        self.assertEqual(report_log.report_type, 'mensual')
        self.assertIsNotNone(report_log.generated_at)
        self.assertTrue((now() - report_log.generated_at).seconds < 1)

    def test_str_representation(self):
        """
        Prueba la representación en cadena del modelo ReportLog.
        """
        report_log = ReportLog.objects.create(user=self.user, report_type='mensual')
        self.assertEqual(str(report_log), f"{self.user} - mensual")

    def test_auto_fecha_creacion(self):
        """
        Prueba que el campo `generated_at` se complete automáticamente.
        """
        report_log = ReportLog.objects.create(user=self.user, report_type='semanal')
        self.assertIsInstance(report_log.generated_at, datetime)

    def test_guardar_y_recuperar_report_log(self):
        """
        Prueba que se pueda guardar y recuperar un registro de ReportLog.
        """
        ReportLog.objects.create(user=self.user, report_type='anual')
        saved_report_logs = ReportLog.objects.all()
        self.assertEqual(saved_report_logs.count(), 1)

        first_report_log = saved_report_logs[0]
        self.assertEqual(first_report_log.user, self.user)
        self.assertEqual(first_report_log.report_type, 'anual')
