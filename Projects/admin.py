from django.contrib import admin
from .models import Project, Milestone, Task, ProjectFreelancer, Application
from django_quill.forms import QuillFormField

# Personalización del modelo Project en el admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'start_date', 'due_date', 'budget', 'created_at')
    search_fields = ('title', 'client__user__username')
    list_filter = ('start_date', 'due_date', 'client')
    ordering = ('-created_at',)

    # Personaliza el formulario del admin
    formfield_overrides = {
        'description': {'widget': QuillFormField},  # Usar el widget de Quill para el campo description
    }

# Personalización del modelo Milestone en el admin
@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'category')
    search_fields = ('title', 'project__title')
    list_filter = ('due_date', 'category')
    ordering = ('-due_date',)

    formfield_overrides = {
        'description': {'widget': QuillFormField},  # Usar el widget de Quill para el campo description
    }

# Personalización del modelo Task en el admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'milestone', 'due_date', 'priority', 'status', 'assigned_to')
    search_fields = ('title', 'milestone__title', 'assigned_to__user__username')
    list_filter = ('due_date', 'priority', 'status')
    ordering = ('-due_date',)

    formfield_overrides = {
        'description': {'widget': QuillFormField},  # Usar el widget de Quill para el campo description
    }

# Personalización del modelo ProjectFreelancer en el admin
@admin.register(ProjectFreelancer)
class ProjectFreelancerAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'status', 'created_at')
    search_fields = ('project__title', 'freelancer__user__username')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

# Personalización del modelo Application en el admin
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'project', 'applied_at')
    search_fields = ('freelancer__user__username', 'project__title')
    list_filter = ('applied_at',)
    ordering = ('-applied_at',)
