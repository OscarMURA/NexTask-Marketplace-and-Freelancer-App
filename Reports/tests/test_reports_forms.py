from django.test import TestCase
from Reports.forms import ReportFilterForm
from datetime import date

class ReportFilterFormTest(TestCase):

    def test_form_valido_con_fechas(self):
        """
        Prueba que el formulario sea válido con fechas válidas.
        """
        form_data = {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        }
        form = ReportFilterForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['start_date'], date(2024, 1, 1))
        self.assertEqual(form.cleaned_data['end_date'], date(2024, 12, 31))

    def test_form_valido_sin_fechas(self):
        """
        Prueba que el formulario sea válido cuando no se proporcionan fechas.
        """
        form = ReportFilterForm(data={})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data['start_date'])
        self.assertIsNone(form.cleaned_data['end_date'])

    def test_form_invalido_fecha_incorrecta(self):
        """
        Prueba que el formulario sea inválido con un formato de fecha incorrecto.
        """
        form_data = {
            'start_date': 'fecha_incorrecta',
            'end_date': '2024-12-31'
        }
        form = ReportFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors)

    def test_form_end_date_anterior_a_start_date(self):
        """
        Prueba un caso donde `end_date` es anterior a `start_date`, si hay validaciones futuras.
        """
        form_data = {
            'start_date': '2024-12-31',
            'end_date': '2024-01-01'
        }
        form = ReportFilterForm(data=form_data)
        self.assertTrue(form.is_valid())  # No hay validación por orden en el formulario base.
