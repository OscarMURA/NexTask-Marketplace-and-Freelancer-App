from django import forms
from Projects.models import Project
from django.core.exceptions import ValidationError


class ReportFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    metrics = forms.MultipleChoiceField(
        choices=[
            ('progress', 'Progress of the Projects'),
            ('budget', 'Budget used'),
            ('milestones', 'Milestones status'), 
            ('tasks', 'Tasks status')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    project = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extrae el usuario de los argumentos
        super().__init__(*args, **kwargs)

        # Verifica si hay un usuario y carga los proyectos correspondientes
        if user:
            projects = Project.objects.filter(client=user.clientprofile)
            self.fields['project'].choices = [(project.id, project.title) for project in projects]
        else:
            self.fields['project'].choices = []  # Si no hay usuario, no muestra proyectos

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        project_id = cleaned_data.get("project")
        
        if start_date and end_date and start_date > end_date:
            self.add_error("start_date", "The start date cannot be after the end date.")
            self.add_error("end_date", "The end date cannot be before the start date.")
            
        if project_id:
            project = Project.objects.get(id=project_id)
            project_start_date = project.start_date  # Ajusta al nombre correcto del campo en el modelo
            project_end_date = project.actual_end_date  # Ajusta al nombre correcto del campo en el modelo
            
            if start_date and start_date < project_start_date:
                self.add_error("start_date", "The start date is before the project start date.")
                
            if end_date and project_end_date and end_date > project_end_date:
                self.add_error("end_date", "The end date is after the project end date.")

        return cleaned_data
