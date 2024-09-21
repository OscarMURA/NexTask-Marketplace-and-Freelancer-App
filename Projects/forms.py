# forms.py
from django import forms
from .models import Project,Milestone, Task
from django_quill.forms import QuillFormField


class ProjectForm(forms.ModelForm):
    description = QuillFormField()
    class Meta:
        model = Project
        fields = ['title', 'start_date', 'due_date', 'description', 'budget','category']
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'category': forms.Select(attrs={'class': 'form-select shadow-none'}),
        }
        
        
class MilestoneForm(forms.ModelForm):
    description = QuillFormField()

    class Meta:
        model = Milestone
        fields = ['title', 'description', 'due_date', 'file','category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'category': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'file': forms.FileInput(attrs={'class': 'form-control shadow-none'}),
            'title': forms.TextInput(attrs={'class': 'form-control shadow-none'}),

        }

class TaskForm(forms.ModelForm):
    description = QuillFormField()

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'priority': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'status': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'title': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
        }