from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import FreelancerSignUpForm, ClientSignUpForm, EducationForm, WorkExperienceForm
from .models import FreelancerProfile, ClientProfile, User
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


# Vista para registrar historial académico
def education_register(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.freelancer = request.user.freelancerprofile
            education.save()
            return redirect('workexperience_register')
    else:
        form = EducationForm()

    # Permitir que el usuario omita esta parte
    if 'skip' in request.GET:
        return redirect('workexperience_register')

    return render(request, 'Users/education_register.html', {'form': form})

def workexperience_register(request):
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            workexperience = form.save(commit=False)
            workexperience.freelancer = request.user.freelancerprofile
            workexperience.save()
            return redirect('profile_view')  # Redirige al perfil o home
    else:
        form = WorkExperienceForm()

    if 'skip' in request.GET:
        return redirect('profile_view')

    return render(request, 'Users/workexperience_register.html', {'form': form})

