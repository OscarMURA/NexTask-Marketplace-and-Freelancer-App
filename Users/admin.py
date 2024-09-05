from django.contrib import admin
from .models import User, FreelancerProfile, ClientProfile, Skill

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city', 'phone', 'address')  # Añadido 'city'
    search_fields = ('user__username', 'country', 'city')  # Añadido 'city'
    list_filter = ('country', 'city')  # Opción para filtrar por país y ciudad

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'country', 'city')  # Añadido 'country' y 'city'
    search_fields = ('user__username', 'company_name', 'country', 'city')  # Añadido 'country' y 'city'
    list_filter = ('country', 'city')  # Opción para filtrar por país y ciudad

admin.site.register(Skill)
