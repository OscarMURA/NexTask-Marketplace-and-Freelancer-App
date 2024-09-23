from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages  # Para los mensajes de error y éxito
from django.contrib.auth.decorators import login_required


@never_cache
def client_signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Usuario creado:", user)  # Imprimir el usuario creado
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home_client')
    else:
        form = ClientSignUpForm()
    return render(request, 'Users/client_signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                auth_login(request, user)  # Usamos auth_login para iniciar sesión
                # Redirigir según el tipo de usuario
                if user.user_type == 'freelancer':
                    return redirect('home_freelancer')
                elif user.user_type == 'client':
                    return redirect('home_client')
            else:
                messages.error(request, 'Invalid username or password.')  # Mensaje en inglés
        else:
            messages.error(request, 'Invalid username or password.')  # Mensaje en inglés
    else:
        form = AuthenticationForm()

    return render(request, 'Users/login.html', {'form': form})

def welcome(request):
    return render(request, 'Users/welcome.html')

def home(request):
    return render(request, 'users/home.html')


from django.contrib.auth import login as auth_login
from django.contrib.auth import get_backends

@never_cache
def freelancer_signup(request):
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Get the default authentication backend (ModelBackend)
            backend = get_backends()[0]  # This assumes the first backend is the correct one
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('work_experience_register')  # Redirect after sign-up
        else:
            print("Form errors:", form.errors)  # Debugging: print form errors to console
    else:
        form = FreelancerSignUpForm()
        
    return render(request, 'Users/freelancer_signup.html', {'form': form})


def work_experience_register_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        formset = WorkExperienceFormSet(request.POST, instance=freelancer)
        if formset.is_valid():
            formset.save()
            return redirect('education_register')
        else:
            print(formset.errors)  # Debugging formset errors
    else:
        formset = WorkExperienceFormSet(instance=freelancer)

    helper = WorkExperienceFormHelper()

    # Debugging: print the management form to check if it's being rendered
    print("Management form:", formset.management_form)

    return render(request, 'Users/work_experience_register.html', {
        'work_experience_formset': formset,
        'helper': helper,
        'back_url': 'register_freelancer',
        'next_url': 'education_register',
    })

@login_required
def education_register_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        formset = EducationFormSet(request.POST, instance=freelancer)
        if formset.is_valid():
            formset.save()
            return redirect('certification_register')
    else:
        formset = EducationFormSet(instance=freelancer)

    helper = EducationFormHelper()

    # Debugging: print the management form to check the formset prefix
    print("Management form:", formset.management_form)

    return render(request, 'Users/education_register.html', {
        'education_formset': formset,
        'helper': helper,
        'back_url': 'work_experience_register',
        'next_url': 'certification_register',
    })



@login_required
def certification_register_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        if 'skip' in request.POST:
            return redirect('portfolio_register')
        formset = CertificationFormSet(request.POST, instance=freelancer)
        if formset.is_valid():
            formset.save()
            return redirect('portfolio_register')
    else:
        formset = CertificationFormSet(instance=freelancer)

    # Add the helper here
    helper = CertificationFormHelper()

    return render(request, 'Users/certification_register.html', {
        'certification_formset': formset,
        'helper': helper,  # Pass the helper to the template
        'back_url': 'education_register',
        'next_url': 'portfolio_register',
    })


@login_required
def portfolio_register_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        if 'skip' in request.POST:
            return redirect('register_languages')
        formset = PortfolioFormSet(request.POST, instance=freelancer)
        if formset.is_valid():
            formset.save()
            return redirect('register_languages')
    else:
        formset = PortfolioFormSet(instance=freelancer)

    # Add the helper here
    helper = PortfolioFormHelper()

    return render(request, 'Users/portfolio_register.html', {
        'portfolio_formset': formset,
        'helper': helper,  # Pass the helper to the template
        'back_url': 'certification_register',
        'next_url': 'welcome',
    })
@login_required
def profile_settings(request):
    return render(request, 'Users/changePassword.html')




@login_required
def register_skills_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        form = SkillsForm(request.POST, instance=freelancer)
        if form.is_valid():
            form.save()
            return redirect('home_freelancer')  # Redirigir al final del flujo, página de bienvenida
    else:
        form = SkillsForm(instance=freelancer)

    return render(request, 'Users/register_skills.html', {'form': form})

@login_required
def register_languages_view(request):
    freelancer = request.user.freelancerprofile
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=freelancer)
        if form.is_valid():
            form.save()
            return redirect('register_skills')  # Redirect to the next step
    else:
        form = LanguageForm(instance=freelancer)

    return render(request, 'Users/register_languages.html', {'form': form})


def home_client(request):
    return render(request, 'Users/homeClient.html')

@login_required
def home_freelancer(request):
    return render(request, 'Users/homeFreelancer.html')

def createProject(request):
    return render(request, 'Users/createProject.html')

def change_password(request):
    return render(request, 'Users/changePassword.html')

@login_required
def profile_settings(request):
   user = request.user
   try:
        freelancer = FreelancerProfile.objects.get(user=user)
   except FreelancerProfile.DoesNotExist:
        freelancer = FreelancerProfile(user=user)
        freelancer.save()  # Crea el perfil si no existe

   if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        city = request.POST.get('city') 
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        freelancer.city = city
        freelancer.country = country
        freelancer.phone = phone
        freelancer.address = address
        freelancer.save()

        messages.success(request, 'Your profile has been updated successfully.')
     
   return render(request, 'Users/profileSettings.html', {'user': user, 'freelancer': freelancer})

