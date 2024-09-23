# forms.py
from django import forms
from .models import Project, Milestone, Task
from django_quill.forms import QuillFormField
from Users.models import FreelancerProfile

class ProjectForm(forms.ModelForm):
    """
    Form for creating and editing projects.

    This form allows users to enter project details,
    including the title, start and due dates, description, budget, and category.
    """
    description = QuillFormField()

    class Meta:
        model = Project
        fields = ['title', 'start_date', 'due_date', 'description', 'budget', 'category']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'category': forms.Select(attrs={'class': 'form-select shadow-none'}),
        }

class MilestoneForm(forms.ModelForm):
    """
    Form for creating and editing milestones within a project.

    This form allows users to enter milestone details,
    including the title, description, due date, attached file, and category.
    """
    description = QuillFormField()

    class Meta:
        model = Milestone
        fields = ['title', 'description', 'due_date', 'file', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'category': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'file': forms.FileInput(attrs={'class': 'form-control shadow-none'}),
            'title': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
        }

class TaskForm(forms.ModelForm):
    """
    Form for creating and editing tasks associated with a milestone.

    This form allows users to enter task details,
    including the title, description, due date, priority,
    status, assigned freelancer, and attachments.
    """
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
        """
        Initializes the form and filters the 'assigned_to' field to show
        only the freelancers available according to the project's association.
        """
        # Get the 'freelancers' argument passed from the view
        freelancers = kwargs.pop('freelancers', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if freelancers is not None:
            # Filter the 'assigned_to' field to show only the freelancers from the contract
            self.fields['assigned_to'].queryset = FreelancerProfile.objects.filter(id__in=[freelancer.id for freelancer in freelancers])
