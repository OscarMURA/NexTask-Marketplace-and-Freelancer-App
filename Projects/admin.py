from django.contrib import admin
from .models import Project
from django_quill.forms import QuillFormField

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
