from django.contrib import admin
from .models import User, FreelancerProfile, ClientProfile, Skill, Certification, Portfolio, Language, Education, WorkExperience

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

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'certification_name', 'issuing_organization', 'issue_date')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'url')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language',)
    search_fields = ('language',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'institution_name', 'degree_obtained', 'start_date', 'end_date')
    search_fields = ('freelancer__user__username', 'institution_name', 'degree_obtained')
    list_filter = ('start_date', 'end_date')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'company_name', 'position', 'start_date', 'end_date')
    search_fields = ('freelancer__user__username', 'company_name', 'position')
    list_filter = ('start_date', 'end_date')

admin.site.register(Skill)
