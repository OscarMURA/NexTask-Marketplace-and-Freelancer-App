from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import FreelancerSignUpForm, ClientSignUpForm
from .models import FreelancerProfile, ClientProfile
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.views.decorators.csrf import csrf_protect


@never_cache
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
@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        user_type = request.POST.get('user_type')  # Obtenemos el tipo de usuario desde el formulario
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Verificamos que el tipo de usuario coincida con el del usuario en la base de datos
                if user.user_type != user_type:
                    messages.error(request, "Selecciona el tipo de usuario correcto.")  # Mostramos mensaje de error
                else:
                    login(request, user)
                    return redirect('welcome')  # Redirige a la página de bienvenida
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    
    else:
        form = AuthenticationForm()

    return render(request, 'Users/login.html', {'form': form})

def welcome(request):
    return HttpResponse('<h1>Bienvenido</h1>')