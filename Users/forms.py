from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.forms import ModelForm, ValidationError, inlineformset_factory
from django_select2.forms import Select2MultipleWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_select2.forms import *
import re
from django.db.models import Count

# Base class for User Signup
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up'))

class FreelancerSignUpForm(UserSignUpForm):
    avatar = forms.ImageField(required=False, label="Profile Picture", help_text="Optional. Upload an image for your profile.")  # Avatar field added

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up as Freelancer'))
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:  # Solo valida si el campo no está vacío
            if not re.match(r'^\+?1?\d{9,15}$', phone):  # Patrón de validación de número de teléfono
                raise ValidationError("El número de celular no es válido. Debe contener entre 9 y 15 dígitos.")
        return phone

    def save(self, commit=True):
        """
        Guardar el usuario y el perfil de freelancer, pero no el formset de certificaciones,
        ya que esto lo manejaremos en las pruebas y vistas donde sea necesario.
        """
        user = super().save(commit=False)
        user.user_type = 'freelancer'
        if commit:
            user.save()
            freelancer_profile = FreelancerProfile.objects.create(
                user=user,
                country=self.cleaned_data.get('country'),
                city=self.cleaned_data.get('city'),
                phone=self.cleaned_data.get('phone'),
                address=self.cleaned_data.get('address'),
            )
            freelancer_profile.save()
            print("Freelancer creado")
        return user

# Form for Client Signup
class ClientSignUpForm(UserSignUpForm):
    avatar = forms.ImageField(required=False, label="Profile Picture", help_text="Optional. Upload an image for your profile.")  # Avatar field added
    company_name = forms.CharField(max_length=255, required=True)
    company_website = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up as Client'))

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
            client_profile.avatar = self.cleaned_data.get('avatar')  # Save avatar
            client_profile.save()
        return user

# Certification Formset
CertificationFormSet = inlineformset_factory(
    FreelancerProfile,
    Certification,
    fields=('certification_name', 'issuing_organization', 'issue_date', 'expiration_date', 'short_description'),
    widgets={
        'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
        'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
        'short_description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),
    },
    extra=1,
    can_delete=True
)

class CertificationFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True

# Portfolio Formset
PortfolioFormSet = inlineformset_factory(
    FreelancerProfile,
    Portfolio,
    fields=('url', 'description'),
    widgets={
        'url': forms.URLInput(attrs={'class': 'form-control shadow-none'}),
        'description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),
    },
    extra=1,
    can_delete=True
)

class PortfolioFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.add_input(Submit('submit', 'Save'))

# Education Formset
EducationFormSet = inlineformset_factory(
    FreelancerProfile,
    Education,
    fields=('institution_name', 'degree_obtained', 'start_date', 'end_date', 'description'),
    widgets={
        'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
        'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
        'description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),
    },
    extra=1,
    can_delete=True
)

class EducationFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.add_input(Submit('submit', 'Save'))

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'position', 'start_date', 'end_date', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = WorkExperienceFormHelper()  # Agrega el helper aquí

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and start_date and end_date < start_date:
            raise ValidationError("La fecha de finalización debe ser posterior a la fecha de inicio.")

        return cleaned_data
    
WorkExperienceFormSet = inlineformset_factory(
    FreelancerProfile,
    WorkExperience,
    form=WorkExperienceForm,  # Añadir esta línea
    fields=('company_name', 'position', 'start_date', 'end_date', 'description'),
    widgets={
        'company_name': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
        'position': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
        'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
        'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),
        'description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),
    },
    extra=1,
    can_delete=True
)


class WorkExperienceFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.add_input(Submit('submit', 'Save'))

class SkillsForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control shadow-none'}),
        required=False
    )
    
    new_skill = forms.CharField(
        max_length=100, 
        required=False, 
        help_text="If you don't see your skill, add it here",
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none'})
    )
    
    class Meta:
        model = FreelancerProfile
        fields = ['skills', 'new_skill']  

    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Guarda las habilidades predefinidas seleccionadas en el perfil del freelancer
        if commit:
            profile.save()
            self.cleaned_data['skills'] = profile.skills.set(self.cleaned_data['skills'])
            
            # Agregar una nueva habilidad si se proporciona y no existe en las predefinidas
            new_skill = self.cleaned_data.get('new_skill')
            if new_skill:
                skill, created = Skill.objects.get_or_create(name=new_skill)
                profile.skills.add(skill)
            profile.save()
            self.save_m2m()

        return profile

class LanguageForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes instead of dropdown
        required=True
    )

    class Meta:
        model = FreelancerProfile
        fields = ['languages']

class FreelancerSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label="Search by username")
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['avatar', 'company_name', 'company_website', 'country', 'city', 'phone', 'address']


class ClientSearchForm(forms.Form):
    keyword = forms.CharField(
        required=False,
        max_length=255,
        label="Search by keyword (company name, city, country)",
        widget=forms.TextInput(attrs={'placeholder': 'Enter keyword...'})
    )
    country = CountryField().formfield(
        required=False,
        widget=CountrySelectWidget(attrs={'class': 'form-control shadow-none'})
    )
