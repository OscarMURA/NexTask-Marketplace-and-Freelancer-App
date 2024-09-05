from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClientProfile, FreelancerProfile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# Formulario para el registro de Freelancers
class FreelancerSignUpForm(UserCreationForm):
    country = CountryField().formfield(
    widget=CountrySelectWidget(attrs={'class': 'form-control shadow-none'})
)
    city = forms.CharField(max_length=255, required=True)  # Añadido campo de ciudad
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'freelancer'
        if commit:
            user.save()
            freelancer_profile = FreelancerProfile.objects.create(user=user)
            freelancer_profile.country = self.cleaned_data.get('country')  # Guardar país
            freelancer_profile.city = self.cleaned_data.get('city')  # Guardar ciudad
            freelancer_profile.phone = self.cleaned_data.get('phone')
            freelancer_profile.address = self.cleaned_data.get('address')
            freelancer_profile.save()
        return user

# Formulario para el registro de Clientes
class ClientSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=True)
    company_website = forms.URLField(required=False)
    country = CountryField().formfield(widget=CountrySelectWidget())  # Correcto uso de CountryField
    city = forms.CharField(max_length=255, required=True)  # Añadido campo de ciudad
    phone = forms.CharField(max_length=20, required=False)  # Añadido teléfono
    address = forms.CharField(max_length=255, required=False)  # Añadida dirección

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
            client_profile = ClientProfile.objects.create(user=user)
            client_profile.company_name = self.cleaned_data.get('company_name')
            client_profile.company_website = self.cleaned_data.get('company_website')
            client_profile.country = self.cleaned_data.get('country')  # Guardar país
            client_profile.city = self.cleaned_data.get('city')  # Guardar ciudad
            client_profile.phone = self.cleaned_data.get('phone')  # Guardar teléfono
            client_profile.address = self.cleaned_data.get('address')  # Guardar dirección
            client_profile.save()
        return user
