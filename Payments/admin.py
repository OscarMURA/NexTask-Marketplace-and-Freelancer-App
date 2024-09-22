# admin.py en Payments
from django.contrib import admin
from .models import *

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('project', 'client', 'freelancer', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'client__user__username', 'freelancer__user__username')
