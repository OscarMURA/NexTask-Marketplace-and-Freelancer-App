# Users/admin.py

from django.contrib import admin
from .models import User, FreelancerProfile, ClientProfile, Skill, AcademicRecord, WorkExperience

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Puedes hacer algo similar con otros modelos si lo necesitas
@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name')
    search_fields = ('user__username', 'company_name')

# Registrar habilidades y otros modelos
admin.site.register(Skill)
admin.site.register(AcademicRecord)
admin.site.register(WorkExperience)
