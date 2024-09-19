# forms.py
from django import forms
from .models import Project
from django_quill.forms import QuillFormField


class ProjectForm(forms.ModelForm):
    description = QuillFormField()
    class Meta:
        model = Project
        fields = ['title', 'start_date', 'due_date', 'description', 'budget']
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
