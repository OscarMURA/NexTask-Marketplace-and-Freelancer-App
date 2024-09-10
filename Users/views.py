from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import FreelancerSignUpForm, ClientSignUpForm, EducationFormSet, WorkExperienceFormSet
from .models import FreelancerProfile, ClientProfile, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages  # Para los mensajes de error y éxito


@never_cache
def freelancer_signup(request):
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Usamos auth_login para evitar conflicto
            return redirect('education_register')  # Redirige al registro de educación
    else:
        form = FreelancerSignUpForm()
    return render(request, 'Users/freelancer_signup.html', {'form': form})

@never_cache
def client_signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Usamos auth_login para evitar conflicto
            return redirect('home')
    else:
        form = ClientSignUpForm()
    return render(request, 'Users/client_signup.html', {'form': form})

# Renombramos la función login a user_login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('welcome')  # Redirige a la página de bienvenida
            else:
                
                messages.error(request, 'El nombre de usuario o la contraseña es incorrecto.')
        else:
            
            messages.error(request, 'El nombre de usuario o la contraseña es incorrecto.')

    else:
        form = AuthenticationForm()

    return render(request, 'Users/login.html', {'form': form})

def welcome(request):
    return render(request, 'Users/welcome.html')

@login_required
def education_register_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        formset = EducationFormSet(request.POST, instance=freelancer)
        if formset.is_valid():
            formset.save()
            return redirect('work_experience_register')  # Redirige al registro de experiencia laboral
    else:
        formset = EducationFormSet(instance=freelancer)

    return render(request, 'Users/education_register.html', {'education_formset': formset})

@login_required
def work_experience_register_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        formset = WorkExperienceFormSet(request.POST, instance=freelancer)
        if formset.is_valid():
            formset.save()
            return redirect('welcome')  # Redirige a la página de bienvenida después de registrar la experiencia laboral
    else:
        formset = WorkExperienceFormSet(instance=freelancer)

    return render(request, 'Users/workexperience_register.html', {'work_experience_formset': formset})