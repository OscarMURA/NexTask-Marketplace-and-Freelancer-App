from django import forms
from Projects.models import Project

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
    
