# forms.py
from django import forms
from .models import Project,Milestone, Task
from django_quill.forms import QuillFormField
from Users.models import FreelancerProfile 



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
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'assigned_to', 'attachments']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'priority': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'status': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'title': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
            'attachments': forms.FileInput(attrs={'class': 'form-control shadow-none'}),
        }
    def __init__(self, *args, **kwargs):
        # Obtener el argumento 'freelancers' que será pasado desde la vista
        freelancers = kwargs.pop('freelancers', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if freelancers is not None:
            # Filtrar el campo 'assigned_to' para mostrar solo los freelancers del contrato
            self.fields['assigned_to'].queryset = FreelancerProfile.objects.filter(id__in=[freelancer.id for freelancer in freelancers])