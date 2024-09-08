from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClientProfile, FreelancerProfile, Education, WorkExperience
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# Clase base para el registro de usuarios
class UserSignUpForm(UserCreationForm):
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control shadow-none'})
    )
    city = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

# Formulario para el registro de Freelancers
class FreelancerSignUpForm(UserSignUpForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'freelancer'
        if commit:
            user.save()
            freelancer_profile = FreelancerProfile.objects.create(user=user)
            freelancer_profile.country = self.cleaned_data.get('country')
            freelancer_profile.city = self.cleaned_data.get('city')
            freelancer_profile.phone = self.cleaned_data.get('phone')
            freelancer_profile.address = self.cleaned_data.get('address')
            freelancer_profile.save()
        return user

# Formulario para el registro de Clientes
class ClientSignUpForm(UserSignUpForm):
    company_name = forms.CharField(max_length=255, required=True)
    company_website = forms.URLField(required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
            client_profile = ClientProfile.objects.create(user=user)
            client_profile.company_name = self.cleaned_data.get('company_name')
            client_profile.company_website = self.cleaned_data.get('company_website')
            client_profile.country = self.cleaned_data.get('country')
            client_profile.city = self.cleaned_data.get('city')
            client_profile.phone = self.cleaned_data.get('phone')
            client_profile.address = self.cleaned_data.get('address')
            client_profile.save()
        return user

# Formulario para registrar historial académico
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution_name', 'degree', 'major', 'start_date', 'end_date', 'short_description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),
        }

# Formulario para registrar historial laboral
class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'position', 'start_date', 'end_date', 'short_description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),
        }
