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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate

# Base class for User Signup
class UserSignUpForm(UserCreationForm):
    """
    Form for user registration that includes country, city, phone, and address fields.

    Attributes:
        country (CountryField): Field for selecting the user's country.
        city (str): City where the user is located.
        phone (str): Phone number of the user.
        address (str): Address of the user.
    """
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control shadow-none'})
    )
    city = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta(UserCreationForm.Meta):
        model = User  # Custom User model
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initializes the form helper for styling and submission.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up'))


# Form for Freelancer Signup
class FreelancerSignUpForm(UserSignUpForm):
    """
    Form for freelancer registration that extends the UserSignUpForm.

    Attributes:
        avatar (ImageField): Optional profile picture field for the freelancer.
    """
    avatar = forms.ImageField(required=False, label="Profile Picture", help_text="Optional. Upload an image for your profile.")  # Avatar field added

    def __init__(self, *args, **kwargs):
        """
        Initializes the form helper for freelancer-specific styling and submission.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up as Freelancer'))
        
        

    def save(self, commit=True):
        """
        Saves the freelancer profile, setting the user type and creating the related FreelancerProfile.

        Args:
            commit (bool): Whether to save the user to the database.

        Returns:
            User: The created user instance.
        """
        user = super().save(commit=False)  # Create user without saving to DB
        user.user_type = 'freelancer'  # Set user type to freelancer
        if commit:
            user.save()  # Save user to DB
            freelancer_profile = FreelancerProfile.objects.create(user=user)
            freelancer_profile.country = self.cleaned_data.get('country')
            freelancer_profile.city = self.cleaned_data.get('city')
            freelancer_profile.phone = self.cleaned_data.get('phone')
            freelancer_profile.address = self.cleaned_data.get('address')
            freelancer_profile.avatar = self.cleaned_data.get('avatar')  # Save avatar
            freelancer_profile.save()
            print("Freelancer created")
        return user


# Form for Client Signup
class ClientSignUpForm(UserSignUpForm):
    """
    Form for client registration that extends the UserSignUpForm.

    Attributes:
        avatar (ImageField): Optional profile picture field for the client.
        company_name (str): Name of the client's company.
        company_website (str): Website of the client's company.
    """
    avatar = forms.ImageField(required=False, label="Profile Picture", help_text="Optional. Upload an image for your profile.")  # Avatar field added
    company_name = forms.CharField(max_length=255, required=True)
    company_website = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes the form helper for client-specific styling and submission.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up as Client'))

    def save(self, commit=True):
        """
        Saves the client profile, setting the user type and creating the related ClientProfile.

        Args:
            commit (bool): Whether to save the user to the database.

        Returns:
            User: The created user instance.
        """
        user = super().save(commit=False)  # Create user without saving to DB
        user.user_type = 'client'  # Set user type to client
        if commit:
            user.save()  # Save user to DB
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

# Helper class for Certification Form
class CertificationFormHelper(FormHelper):
    """
    Helper class for the Certification Form to customize its rendering.

    Attributes:
        form_method (str): The method to use for form submission (POST).
        render_required_fields (bool): Indicates whether to render required fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'  # Set form method to POST
        self.render_required_fields = True  # Render required fields


# Portfolio Formset
PortfolioFormSet = inlineformset_factory(
    FreelancerProfile,
    Portfolio,
    fields=('url', 'description'),  # Fields to include in the formset
    widgets={
        'url': forms.URLInput(attrs={'class': 'form-control shadow-none'}),  # URL input styling
        'description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),  # Description textarea styling
    },
    extra=1,  # Number of extra empty forms to display
    can_delete=True  # Allow deletion of forms in the formset
)

# Helper class for Portfolio Form
class PortfolioFormHelper(FormHelper):
    """
    Helper class for the Portfolio Form to customize its rendering.

    Attributes:
        form_method (str): The method to use for form submission (POST).
        render_required_fields (bool): Indicates whether to render required fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'  # Set form method to POST
        self.render_required_fields = True  # Render required fields
        self.add_input(Submit('submit', 'Save'))  # Add a submit button


# Education Formset
EducationFormSet = inlineformset_factory(
    FreelancerProfile,
    Education,
    fields=('institution_name', 'degree_obtained', 'start_date', 'end_date', 'description'),  # Fields to include in the formset
    widgets={
        'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),  # Start date input styling
        'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),  # End date input styling
        'description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),  # Description textarea styling
    },
    extra=1,  # Number of extra empty forms to display
    can_delete=True  # Allow deletion of forms in the formset
)

# Helper class for Education Form
class EducationFormHelper(FormHelper):
    """
    Helper class for the Education Form to customize its rendering.

    Attributes:
        form_method (str): The method to use for form submission (POST).
        render_required_fields (bool): Indicates whether to render required fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'  # Set form method to POST
        self.render_required_fields = True  # Render required fields
        self.add_input(Submit('submit', 'Save'))  # Add a submit button


# Work Experience Formset
WorkExperienceFormSet = inlineformset_factory(
    FreelancerProfile,
    WorkExperience,
    fields=('company_name', 'position', 'start_date', 'end_date', 'description'),  # Fields to include in the formset
    widgets={
        'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),  # Start date input styling
        'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-none'}),  # End date input styling
        'description': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': 3}),  # Description textarea styling
    },
    extra=1,  # Number of extra empty forms to display
    can_delete=True  # Allow deletion of forms in the formset
)


class WorkExperienceFormHelper(FormHelper):
    """
    Helper class for the Work Experience Form to customize its rendering.

    Attributes:
        form_method (str): The method to use for form submission (POST).
        render_required_fields (bool): Indicates whether to render required fields.
        add_input (Submit): Adds a submit button to the form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'  # Set form method to POST
        self.render_required_fields = True  # Render required fields
        self.add_input(Submit('submit', 'Save'))  # Add a submit button


class SkillsForm(forms.ModelForm):
    """
    Form for managing the skills of a freelancer.

    Fields:
        skills (ModelMultipleChoiceField): A field to select predefined skills.
        new_skill (CharField): A field to add a new skill that isn't predefined.
    """
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control shadow-none'}),  # Multiple select for skills
        required=False
    )
    
    new_skill = forms.CharField(
        max_length=100, 
        required=False, 
        help_text="If you don't see your skill, add it here",
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none'})  # Input for new skill
    )
    
    class Meta:
        model = FreelancerProfile
        fields = ['skills', 'new_skill']  # Fields to include in the form

    def save(self, commit=True):
        profile = super().save(commit=False)  # Prevent saving until we customize

        if commit:
            profile.save()  # Save the freelancer profile
            self.cleaned_data['skills'] = profile.skills.set(self.cleaned_data['skills'])  # Set selected skills
            
            # Add a new skill if provided and it doesn't exist in the predefined list
            new_skill = self.cleaned_data.get('new_skill')
            if new_skill:
                skill, created = Skill.objects.get_or_create(name=new_skill)  # Create new skill if not exists
                profile.skills.add(skill)  # Add new skill to the profile
            profile.save()  # Save the profile again
            self.save_m2m()  # Save many-to-many relationships

        return profile  # Return the updated profile


class LanguageForm(forms.ModelForm):
    """
    Form for selecting languages for a freelancer.

    Fields:
        languages (ModelMultipleChoiceField): A field to select multiple languages using checkboxes.
    """
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for selection
        required=True
    )

    class Meta:
        model = FreelancerProfile
        fields = ['languages']  # Field to include in the form


class FreelancerSearchForm(forms.Form):
    """
    Form for searching freelancers.

    Fields:
        keyword (CharField): A field to search by username.
        skills (ModelMultipleChoiceField): A field to select skills for filtering freelancers.
    """
    keyword = forms.CharField(required=False, label="Search by username")  # Optional keyword for search
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)  # Skills selection


class ClientProfileForm(forms.ModelForm):
    """
    Form for managing client profiles.

    Fields:
        avatar (ImageField): Profile picture.
        company_name (CharField): Name of the company.
        company_website (URLField): Website of the company.
        country (CountryField): Country of the client.
        city (CharField): City of the client.
        phone (CharField): Phone number of the client.
        address (CharField): Address of the client.
    """
    class Meta:
        model = ClientProfile
        fields = ['avatar', 'company_name', 'company_website', 'country', 'city', 'phone', 'address']  # Fields to include


class ClientSearchForm(forms.Form):
    """
    Form for searching clients.

    Fields:
        keyword (CharField): A field to search by keyword (e.g., company name, city, country).
        country (CountryField): A field to filter by country.
    """
    keyword = forms.CharField(
        required=False,
        max_length=255,
        label="Search by keyword (company name, city, country)",
        widget=forms.TextInput(attrs={'placeholder': 'Enter keyword...'})  # Placeholder text for the input
    )
    country = CountryField().formfield(
        required=False,
        widget=CountrySelectWidget(attrs={'class': 'form-control shadow-none'})  # Country selection styling
    )

# Formulario para cambiar la contraseña
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        # Aplicar la clase CSS a cada campo relevante
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        user = self.user
        if not user.check_password(old_password):
            raise ValidationError("Your current password is incorrect.")
        return old_password