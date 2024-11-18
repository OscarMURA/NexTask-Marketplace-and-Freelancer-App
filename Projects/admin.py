# Projects/admin.py

from django.contrib import admin
from .models import Project, Milestone, Task, ProjectFreelancer, Application
from django_quill.forms import QuillFormField
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

# Personalización del modelo Project en el admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'start_date', 'due_date', 'budget', 'is_deleted', 'created_at')
    search_fields = ('title', 'client__user__username')
    list_filter = ('start_date', 'due_date', 'client', 'is_deleted', 'category')
    ordering = ('-created_at',)
    actions = ['restore_projects', 'permanently_delete_projects']
    
    formfield_overrides = {
        'description': {'widget': QuillFormField},  # Usar el widget de Quill para el campo description
    }

    def get_queryset(self, request):
        # Mostrar todos los proyectos, incluidos los eliminados
        return Project.all_objects.all()

    def restore_projects(self, request, queryset):
        """
        Acción personalizada para restaurar proyectos eliminados.
        """
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} proyecto(s) restaurado(s) exitosamente.", messages.SUCCESS)

    restore_projects.short_description = "Restaurar proyectos seleccionados"

    def permanently_delete_projects(self, request, queryset):
        """
        Acción personalizada para eliminar permanentemente proyectos.
        """
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} proyecto(s) eliminado(s) permanentemente.", messages.WARNING)

    permanently_delete_projects.short_description = "Eliminar permanentemente proyectos seleccionados"


# Personalización del modelo Milestone en el admin
@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'category', 'is_deleted')
    search_fields = ('title', 'project__title')
    list_filter = ('due_date', 'category', 'is_deleted')
    ordering = ('-due_date',)
    actions = ['restore_milestones', 'permanently_delete_milestones']
    
    formfield_overrides = {
        'description': {'widget': QuillFormField},  # Usar el widget de Quill para el campo description
    }

    def get_queryset(self, request):
        # Mostrar todos los hitos, incluidos los eliminados
        return Milestone.all_objects.all()

    def restore_milestones(self, request, queryset):
        """
        Acción personalizada para restaurar hitos eliminados.
        """
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} hito(s) restaurado(s) exitosamente.", messages.SUCCESS)

    restore_milestones.short_description = "Restaurar hitos seleccionados"

    def permanently_delete_milestones(self, request, queryset):
        """
        Acción personalizada para eliminar permanentemente hitos.
        """
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} hito(s) eliminado(s) permanentemente.", messages.WARNING)

    permanently_delete_milestones.short_description = "Eliminar permanentemente hitos seleccionados"


# Personalización del modelo Task en el admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'milestone', 'due_date', 'priority', 'status', 'assigned_to', 'is_deleted')
    search_fields = ('title', 'milestone__title', 'assigned_to__user__username')
    list_filter = ('due_date', 'priority', 'status', 'is_deleted')
    ordering = ('-due_date',)
    actions = ['restore_tasks', 'permanently_delete_tasks']
    
    formfield_overrides = {
        'description': {'widget': QuillFormField},  # Usar el widget de Quill para el campo description
    }

    def get_queryset(self, request):
        # Mostrar todas las tareas, incluidas las eliminadas
        return Task.all_objects.all()

    def restore_tasks(self, request, queryset):
        """
        Acción personalizada para restaurar tareas eliminadas.
        """
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f"{updated} tarea(s) restaurada(s) exitosamente.", messages.SUCCESS)

    restore_tasks.short_description = "Restaurar tareas seleccionadas"

    def permanently_delete_tasks(self, request, queryset):
        """
        Acción personalizada para eliminar permanentemente tareas.
        """
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} tarea(s) eliminado(s) permanentemente.", messages.WARNING)

    permanently_delete_tasks.short_description = "Eliminar permanentemente tareas seleccionadas"


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
