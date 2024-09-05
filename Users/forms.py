# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Skill, FreelancerProfile, AcademicRecord, WorkExperience, ClientProfile

class FreelancerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    new_skill = forms.CharField(max_length=100, required=False, help_text="Add a new skill if not listed.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'freelancer'
        if commit:
            user.save()
            freelancer_profile = FreelancerProfile.objects.create(user=user)
            skills = self.cleaned_data.get('skills')
            new_skill_name = self.cleaned_data.get('new_skill')
            if skills:
                freelancer_profile.skills.set(skills)
            if new_skill_name:
                new_skill, created = Skill.objects.get_or_create(name=new_skill_name)
                freelancer_profile.skills.add(new_skill)
        return user

class ClientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=255)
    company_website = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'client'
        if commit:
            user.save()
            client_profile = ClientProfile.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                company_website=self.cleaned_data.get('company_website')
            )
        return user
