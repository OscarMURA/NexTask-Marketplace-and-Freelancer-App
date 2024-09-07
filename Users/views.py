from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import FreelancerSignUpForm, ClientSignUpForm
from .models import FreelancerProfile, ClientProfile
from django.views.decorators.cache import never_cache

def freelancer_signup(request):
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Usamos auth_login para evitar conflicto
            return redirect('register_freelancer')
    else:
        form = FreelancerSignUpForm()
    return render(request, 'Users/freelancer_signup.html', {'form': form})

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
        # Procesar el formulario de inicio de sesión
        pass
    return render(request, 'Users/login.html')
