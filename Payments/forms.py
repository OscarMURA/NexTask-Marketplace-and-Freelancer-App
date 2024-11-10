# Payments/forms.py

from django import forms
from .models import OneTimePayment, RecurringPayment

class OneTimePaymentForm(forms.ModelForm):
    """Formulario para crear y editar pagos puntuales."""
    
    class Meta:
        model = OneTimePayment
        fields = ['amount', 'date', 'description']


class RecurringPaymentForm(forms.ModelForm):
    """Formulario para crear y editar pagos periódicos."""
    
    class Meta:
        model = RecurringPayment
        fields = ['amount', 'frequency', 'start_date', 'end_date', 'description']
