from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login

from Payments.models import Payment
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages  # Para los mensajes de error y éxito
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend 
from .models import FreelancerProfile, Skill, Certification, WorkExperience, Portfolio, Language,ClientProfile
from django.db.models import Q, Value
from django.db.models.functions import Concat
from Projects.models import *
from Projects.models import Application
from django.utils.translation import gettext as _
from django_countries import countries
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from urllib.parse import urlencode  # Importa urlencode para agregar parámetros a la URL
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Comments.forms import FreelancerCommentForm
from Comments.models import FreelancerComment
from django.db.models import Avg
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from .models import FreelancerProfile, ClientProfile

@never_cache
def freelancer_signup(request):
    """
    View for handling freelancer signup.

    If the request is a POST, it processes the signup form.
    On successful signup, the user is logged in and redirected to the work experience registration page.
    If there are errors, they are displayed on the signup form.

    Returns:
        Rendered template for freelancer signup with the form.
    """
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST, request.FILES)  # Include file uploads
        if form.is_valid():
            user = form.save()  # Save the new user

            # Explicitly log in the user after signup
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, 'Account created successfully. Welcome!')  # Success message
            return redirect('work_experience_register')  # Redirect to work experience registration
        else:
            messages.error(request, "Please fix the errors below.")  # Error message if form is invalid
    else:
        form = FreelancerSignUpForm()  # Create a new form instance

    return render(request, 'Users/freelancer_signup.html', {'form': form})  # Render signup template


@never_cache
def client_signup(request):
    """
    View for handling client signup.

    If the request is a POST, it processes the signup form.
    On successful signup, the user is logged in and redirected to the client home page.

    Returns:
        Rendered template for client signup with the form.
    """
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST, request.FILES)  # Include file uploads
        if form.is_valid():
            user = form.save()  # Save the new user
            print("Usuario creado:", user)  # Log the created user
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Log in the user
            return redirect('home_client')  # Redirect to client home page
    else:
        form = ClientSignUpForm()  # Create a new form instance
    return render(request, 'Users/client_signup.html', {'form': form})  # Render signup template


def user_login(request):
    """
    View for handling user login.

    If the request is a POST, it processes the login form.
    On successful login, the user is redirected to their respective home page based on user type.
    If the credentials are invalid, an error message is displayed.

    Returns:
        Rendered template for user login with the form.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Create an authentication form with POST data
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Get the cleaned username
            password = form.cleaned_data.get('password')  # Get the cleaned password
            user = authenticate(username=username, password=password)  # Authenticate the user
            
            if user is not None:
                auth_login(request, user)  # Log in the user

                # Redirect to the 'next' URL if present, otherwise redirect based on user type
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    if user.user_type == 'freelancer':
                        return redirect('home_freelancer')  # Redirect to freelancer home
                    elif user.user_type == 'client':
                        return redirect('home_client')  # Redirect to client home
            else:
                messages.error(request, 'Invalid username or password.')  # Error message for invalid credentials
        else:
            messages.error(request, 'Invalid username or password.')  # Error message if form is invalid
    else:
        form = AuthenticationForm()  # Create a new form instance

    return render(request, 'Users/login.html', {'form': form})  # Render login template


def welcome(request):
    """
    View for rendering the welcome page.

    Returns:
        Rendered welcome template.
    """
    return render(request, 'Users/welcome.html')  # Render welcome template


def home(request):
    """
    View for rendering the user home page.

    Returns:
        Rendered home template for users.
    """
    return render(request, 'users/home.html')  # Render home template


@never_cache
def freelancer_signup(request):
    """
    Duplicate view for handling freelancer signup.
    
    This is an identical implementation to the previous freelancer_signup function. 
    It includes handling of file uploads and user login after successful signup.
    
    Returns:
        Rendered template for freelancer signup with the form.
    """
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST, request.FILES)  # Include file uploads
        if form.is_valid():
            user = form.save()  # Save the new user
            auth_login(request, user)  # Log in the user to avoid conflicts
            return redirect('work_experience_register')  # Redirect to work experience registration
    else:
        form = FreelancerSignUpForm()  # Create a new form instance
    return render(request, 'Users/freelancer_signup.html', {'form': form})  # Render signup template


@login_required
def work_experience_register_view(request):
    """
    View for registering work experience for a freelancer.

    This view handles both GET and POST requests. 
    On a POST request, it processes the WorkExperienceFormSet and saves it if valid.
    On a GET request, it initializes the formset with the freelancer's instance.

    Returns:
        Rendered template for work experience registration with the formset and helpers.
    """
    freelancer = request.user.freelancer_profile  # Get the freelancer's profile
    if request.method == "POST":
        formset = WorkExperienceFormSet(request.POST, instance=freelancer)  # Initialize formset with POST data
        if formset.is_valid():
            formset.save()  # Save the formset if valid
            return redirect('education_register')  # Redirect to education registration
        else:
            print(formset.errors)  # Debugging: print formset errors
    else:
        formset = WorkExperienceFormSet(instance=freelancer)  # Initialize formset for GET request

    helper = WorkExperienceFormHelper()  # Initialize form helper

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
    """
    View for registering education for a freelancer.

    This view handles both GET and POST requests. 
    On a POST request, it processes the EducationFormSet and saves it if valid.
    On a GET request, it initializes the formset with the freelancer's instance.

    Returns:
        Rendered template for education registration with the formset and helpers.
    """
    freelancer = request.user.freelancer_profile  # Get the freelancer's profile
    if request.method == "POST":
        formset = EducationFormSet(request.POST, instance=freelancer)  # Initialize formset with POST data
        if formset.is_valid():
            formset.save()  # Save the formset if valid
            return redirect('certification_register')  # Redirect to certification registration
    else:
        formset = EducationFormSet(instance=freelancer)  # Initialize formset for GET request

    helper = EducationFormHelper()  # Initialize form helper

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
    """
    View for registering certifications for a freelancer.

    This view handles both GET and POST requests. 
    On a POST request, it processes the CertificationFormSet and saves it if valid.
    It also allows skipping the certification step.

    Returns:
        Rendered template for certification registration with the formset and helpers.
    """
    freelancer = request.user.freelancer_profile  # Get the freelancer's profile
    if request.method == "POST":
        if 'skip' in request.POST:
            return redirect('portfolio_register')  # Skip to portfolio registration
        formset = CertificationFormSet(request.POST, instance=freelancer)  # Initialize formset with POST data
        if formset.is_valid():
            formset.save()  # Save the formset if valid
            return redirect('portfolio_register')  # Redirect to portfolio registration
    else:
        formset = CertificationFormSet(instance=freelancer)  # Initialize formset for GET request

    helper = CertificationFormHelper()  # Initialize form helper

    return render(request, 'Users/certification_register.html', {
        'certification_formset': formset,
        'helper': helper,  # Pass the helper to the template
        'back_url': 'education_register',
        'next_url': 'portfolio_register',
    })


@login_required
def portfolio_register_view(request):
    """
    View for registering portfolio items for a freelancer.

    This view handles both GET and POST requests. 
    On a POST request, it processes the PortfolioFormSet and saves it if valid.
    It also allows skipping the portfolio step.

    Returns:
        Rendered template for portfolio registration with the formset and helpers.
    """
    freelancer = request.user.freelancer_profile  # Get the freelancer's profile
    if request.method == "POST":
        if 'skip' in request.POST:
            return redirect('register_languages')  # Skip to language registration
        formset = PortfolioFormSet(request.POST, instance=freelancer)  # Initialize formset with POST data
        if formset.is_valid():
            formset.save()  # Save the formset if valid
            return redirect('register_languages')  # Redirect to language registration
    else:
        formset = PortfolioFormSet(instance=freelancer)  # Initialize formset for GET request

    helper = PortfolioFormHelper()  # Initialize form helper

    return render(request, 'Users/portfolio_register.html', {
        'portfolio_formset': formset,
        'helper': helper,  # Pass the helper to the template
        'back_url': 'certification_register',
        'next_url': 'register_languages',
    })

@login_required
def register_skills_view(request):
    """
    View for registering skills for a freelancer.

    This view handles both GET and POST requests. 
    On a POST request, it processes selected predefined skills and new skills entered by the user. 
    It updates the freelancer's skills accordingly.

    Returns:
        Rendered template for skill registration or redirects to the freelancer home page.
    """
    freelancer = request.user.freelancer_profile  # Get the freelancer's profile
    if request.method == "POST":
        # Process selected predefined skills
        selected_skills_ids = request.POST.get('skills', '')
        if selected_skills_ids:
            selected_skills_ids = [int(id) for id in selected_skills_ids.split(',') if id.isdigit()]

        # Process new skills entered by the user
        new_skills = request.POST.get('new_skills', '').split(',')

        # Update selected predefined skills
        if selected_skills_ids:
            freelancer.skills.set(selected_skills_ids)  # Update predefined skills

        # Add new skills
        for skill_name in new_skills:
            skill_name = skill_name.strip()
            if skill_name:
                skill, created = Skill.objects.get_or_create(name=skill_name)  # Create or get the skill
                freelancer.skills.add(skill)  # Add new skill to the freelancer's profile

        freelancer.save()  # Save changes
        return redirect('home_freelancer')  # Redirect to freelancer home page

    else:
        form = SkillsForm(instance=freelancer)  # Initialize form for GET request
        form.fields['skills'].queryset = Skill.objects.all().order_by('name')[:10]  # Limit to the first 10 skills
        return render(request, 'Users/register_skills.html', {'form': form})


@login_required
def register_languages_view(request):
    """
    View for registering languages for a freelancer.

    This view handles both GET and POST requests. 
    On a POST request, it processes the LanguageForm and saves it if valid.
    On a GET request, it initializes the form with the freelancer's instance.

    Returns:
        Rendered template for language registration or redirects to skills registration.
    """
    freelancer = request.user.freelancer_profile  # Get the freelancer's profile
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=freelancer)  # Initialize form with POST data
        if form.is_valid():
            form.save()  # Save the form if valid
            return redirect('register_skills')  # Redirect to skills registration
    else:
        form = LanguageForm(instance=freelancer)  # Initialize form for GET request

    return render(request, 'Users/register_languages.html', {'form': form})


def home_client(request):
    """
    View for rendering the home page for clients.

    Returns:
        Rendered template for client home page.
    """
    return render(request, 'Users/homeClient.html')  # Render client home template

@login_required
def home_freelancer(request):
    """
    View for rendering the home page for freelancers.

    This view retrieves the active contracts associated with the freelancer 
    and the corresponding projects. It counts the number of projects.

    Returns:
        Rendered template for freelancer home page with project information.
    """
    freelancer_profile = request.user.freelancer_profile  # Get the freelancer's profile
    # Get active contracts associated with the freelancer
    active_contracts = Contract.objects.filter(freelancer=freelancer_profile, status='active')
    # Get projects associated with those contracts
    projects = [contract.project for contract in active_contracts]
    total_projects = len(projects)  # Count projects

    pending_payments_count = Payment.objects.filter(freelancer=freelancer_profile, status='pending').count()
    completed_payments_count = Payment.objects.filter(freelancer=freelancer_profile, status='paid').count()
    
    return render(request, 'Users/homeFreelancer.html', {
        'projects': projects,
        'total_projects': total_projects,
        'pending_payments_count': pending_payments_count,
        'completed_payments_count': completed_payments_count,
    })


def createProject(request):
    """
    View for rendering the project creation page.

    Returns:
        Rendered template for creating a project.
    """
    return render(request, 'Users/createProject.html')  # Render project creation template

@login_required
def change_password_client(request):
    """
    View for rendering the change password page for users (clients).

    Returns:
        Rendered template for changing the user's password.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Mantener la sesión activa después de cambiar la contraseña
            messages.success(request, 'Your password has been updated successfully!')
            return render(request, 'Users/changePasswordClient.html', {
                'form': form,
                'show_modal': True,  # Mostrar modal si la contraseña se actualizó correctamente
                'is_submitted': True,
            })
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'Users/changePasswordClient.html', {
                'form': form,
                'show_modal': False,  # No mostrar modal si hubo errores
                'is_submitted': True,
            })
    else:
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'Users/changePasswordClient.html', {
            'form': form,
            'show_modal': False,  # No mostrar modal en la primera carga
            'is_submitted': False,
        })


@login_required
def change_password_freelancer(request):
    """
    View for rendering the change password page for users (freelancers).

    Returns:
        Rendered template for changing the user's password.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Mantener la sesión activa después de cambiar la contraseña
            messages.success(request, 'Your password has been updated successfully!')
            return render(request, 'Users/changePasswordFreelancer.html', {
                'form': form,
                'show_modal': True,  # Mostrar modal si la contraseña se actualizó correctamente
                'is_submitted': True,
            })
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'Users/changePasswordFreelancer.html', {
                'form': form,
                'show_modal': False,  # No mostrar modal si hubo errores
                'is_submitted': True,
            })
    else:
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'Users/changePasswordFreelancer.html', {
            'form': form,
            'show_modal': False,  # No mostrar modal en la primera carga
            'is_submitted': False,
        })


def password_recovery(request):
    storage = messages.get_messages(request)
    for _ in storage:  # Esto fuerza la evaluación y marca los mensajes como usados
        pass

    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email__iexact=email).first()

        if user:
            # Verificar si el usuario es freelancer o cliente para obtener el perfil
            if hasattr(user, 'freelancer_profile'):
                profile = user.freelancer_profile
            elif hasattr(user, 'clientprofile'):
                profile = user.clientprofile
            else:
                messages.error(request, 'No profile associated with this email.')
                return render(request, 'Users/passwordRecovery.html')

            # Generar un código de verificación aleatorio
            verification_code = get_random_string(length=6, allowed_chars='0123456789')
            
            # Almacenar el código de verificación en el perfil del usuario
            profile.verification_code = verification_code  # Asegúrate de tener este campo en tu modelo
            profile.save()

            # Enviar correo con el código de verificación
            subject = "Password Recovery Code"
            message = f"Your password recovery code is: {verification_code}"
            send_mail(subject, message, 'no-reply@yourapp.com', [email])

            # Redirigir al formulario de verificación del código
            return redirect('verify_code', user_id=user.id)
        else:
            messages.error(request, 'Email not found.', extra_tags='password_recovery')


    return render(request, 'Users/passwordRecovery.html')


def verify_code(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        verification_code = request.POST.get('verification_code')

        # Verificar si el usuario es freelancer o cliente para acceder al perfil correcto
        if hasattr(user, 'freelancer_profile'):
            profile = user.freelancer_profile
        elif hasattr(user, 'clientprofile'):
            profile = user.clientprofile
        else:
            messages.error(request, 'No profile associated with this user.')
            return render(request, 'Users/verify_code.html')

        # Verificar si el código coincide con el guardado en el perfil
        if profile.verification_code == verification_code:
            # El código es correcto, redirigir a la página de cambio de contraseña
            return redirect('reset_password', user_id=user.id)
        else:
            messages.error(request, 'Invalid verification code.')
    
    return render(request, 'Users/verify_code.html', {'user_id': user_id})


def reset_password(request, user_id):
    """
    View for resetting the password after verifying the code.
    """
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SetPasswordForm(user)

    return render(request, 'Users/reset_password.html', {'form': form})
    

@login_required
def profile_settings_freelancer(request):
    """
    View for managing the profile settings of a freelancer.

    This view allows the user to update their personal information, 
    as well as manage their education, certifications, work experience, 
    portfolio entries, and skills. 

    It handles both GET and POST requests:
    - On a GET request, it retrieves the freelancer's profile data.
    - On a POST request, it processes the form data for updates and additions.

    Returns:
        Rendered template for profile settings, along with the user's data and relevant messages.
    """
    user = request.user  # Get the currently logged-in user
    try:
        # Try to retrieve the freelancer profile associated with the user
        freelancer = FreelancerProfile.objects.get(user=user)
        # Retrieve related data
        educations = freelancer.educations.all()  # Get all education records for the freelancer
        certifications = Certification.objects.filter(freelancer=freelancer)  # Get certifications
        work_experiences = WorkExperience.objects.filter(freelancer=freelancer)  # Get work experiences
        portfolios = Portfolio.objects.filter(freelancer=freelancer)  # Get portfolio entries
        skills = freelancer.skills.all()  # Get all skills associated with the freelancer
        languages = freelancer.languages.all()  # Get all languages associated with the freelancer
        print("Total languages loaded:", languages.count())  # Para confirmar cuántos idiomas se están recuperando
        print(languages)  # Imprimirá los objetos de idioma asociados al freelancer
        print("Languages from the model: ", languages)  # Esto debería mostrar los objetos del modelo
        for lang in languages:
            print("Language name: ", lang.language)  # Asegúrate de que esto imprime los nombres correctamente
        



    except FreelancerProfile.DoesNotExist:
        # Create a new FreelancerProfile if it does not exist
        freelancer = FreelancerProfile.objects.create(user=user)
        # Initialize empty lists for related data
        educations = []
        certifications = []
        work_experiences = []
        portfolios = []
        skills = []
        languages = []
        print(languages)  # Imprimirá los objetos de idioma asociados al freelancer
    
    all_languages = Language.objects.exclude(id__in=languages.values_list('id', flat=True))
    print("Idiomas registrados: ", [lang.language for lang in languages])
    print("Idiomas para añadir: ", [lang.language for lang in all_languages])

    show_add_modal = request.session.pop('show_add_modal', False)
    show_delete_modal = request.session.pop('show_delete_modal', False)
    show_update_modal = request.session.pop('show_update_modal', False)


    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'add_languages' in request.POST:
            selected_language_ids = request.POST.getlist('languages')
            if selected_language_ids:
                selected_languages = Language.objects.filter(id__in=selected_language_ids)
                freelancer.languages.add(*selected_languages)
                freelancer.save()
                
                show_add_modal = True
                
                # Prepare a list of the new language names to return in the response
                new_languages = [lang.language for lang in selected_languages]
                
                return JsonResponse({
                    'success': True,
                    'new_languages': new_languages,
                    'show_add_modal': show_add_modal
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Please select at least one language.'
                })


        # Check which form is being submitted
        if 'update_user_info' in request.POST:
            # Update user info (first name, last name, email, username)
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.username = request.POST.get('username', user.username)
            user.save()  # Save updated user info

            # Update freelancer profile info (phone, city, country, address)
            freelancer.phone = request.POST.get('phone', freelancer.phone)
            freelancer.city = request.POST.get('city', freelancer.city)
            freelancer.country = request.POST.get('country', freelancer.country)
            freelancer.address = request.POST.get('address', freelancer.address)
            freelancer.save()  # Save updated freelancer info

            show_update_modal = True


        elif 'add_education' in request.POST:
            # Add new education record
            if request.POST.get('new_institution_name') and request.POST.get('new_degree_obtained'):
                new_education = Education(
                    freelancer=freelancer,
                    institution_name=request.POST.get('new_institution_name'),
                    degree_obtained=request.POST.get('new_degree_obtained'),
                    start_date=request.POST.get('new_start_date'),
                    end_date=request.POST.get('new_end_date'),
                    description=request.POST.get('new_description')
                )
                new_education.save()  # Save new education record
                
                request.session['show_add_modal'] = True
                return redirect('profile_settings_freelancer')

        elif 'delete_education' in request.POST:
            # Delete education record
            education_id = request.POST.get('delete_education')
            try:
                education = Education.objects.get(id=education_id, freelancer=freelancer)
                education.delete()  # Delete the education record

                request.session['show_delete_modal'] = True
                return redirect('profile_settings_freelancer')
                
            except Education.DoesNotExist:
                messages.error(request, 'The education record could not be found.')  # Error message

        elif 'add_certification' in request.POST:
            # Add new certification
            if request.POST.get('new_certification_name') and request.POST.get('new_issuing_organization'):
                new_certification = Certification(
                    freelancer=freelancer,
                    certification_name=request.POST.get('new_certification_name'),
                    issuing_organization=request.POST.get('new_issuing_organization'),
                    issue_date=request.POST.get('new_issue_date'),
                    expiration_date=request.POST.get('new_expiration_date'),
                    short_description=request.POST.get('new_certification_description')
                )
                new_certification.save()  # Save new certification
                
                request.session['show_add_modal'] = True
                return redirect('profile_settings_freelancer')


        elif 'delete_certification' in request.POST:
            # Delete certification
            certification_id = request.POST.get('delete_certification')
            try:
                certification = Certification.objects.get(id=certification_id, freelancer=freelancer)
                certification.delete()  # Delete the certification
                
                request.session['show_delete_modal'] = True
                return redirect('profile_settings_freelancer')

            except Certification.DoesNotExist:
                messages.error(request, 'The certification could not be found.')  # Error message

        elif 'add_experience' in request.POST:
            # Add new work experience
            if request.POST.get('new_company_name') and request.POST.get('new_position'):
                new_experience = WorkExperience(
                    freelancer=freelancer,
                    company_name=request.POST.get('new_company_name'),
                    position=request.POST.get('new_position'),
                    start_date=request.POST.get('new_experience_start_date'),
                    end_date=request.POST.get('new_experience_end_date'),
                    description=request.POST.get('new_experience_description')
                )
                new_experience.save()  # Save new work experience
                
                request.session['show_add_modal'] = True
                return redirect('profile_settings_freelancer')

        elif 'delete_experience' in request.POST:
            # Delete work experience
            experience_id = request.POST.get('delete_experience')
            try:
                experience = WorkExperience.objects.get(id=experience_id, freelancer=freelancer)
                experience.delete()  # Delete the work experience
                
                request.session['show_delete_modal'] = True
                return redirect('profile_settings_freelancer')


            except WorkExperience.DoesNotExist:
                messages.error(request, 'The work experience could not be found.')  # Error message

        elif 'add_portfolio' in request.POST:
            # Add new portfolio entry
            if request.POST.get('new_portfolio_url') and request.POST.get('new_portfolio_description'):
                new_portfolio = Portfolio(
                    freelancer=freelancer,
                    url=request.POST.get('new_portfolio_url'),
                    description=request.POST.get('new_portfolio_description')
                )
                new_portfolio.save()  # Save new portfolio entry
                
                request.session['show_add_modal'] = True
                return redirect('profile_settings_freelancer')


        elif 'delete_portfolio' in request.POST:
            # Delete portfolio entry
            portfolio_id = request.POST.get('delete_portfolio')
            try:
                portfolio = Portfolio.objects.get(id=portfolio_id, freelancer=freelancer)
                portfolio.delete()  # Delete the portfolio entry

                request.session['show_delete_modal'] = True
                return redirect('profile_settings_freelancer')

            except Portfolio.DoesNotExist:
                messages.error(request, 'The portfolio entry could not be found.')  # Error message
        
       
        # Process skills
        selected_skills_ids = request.POST.getlist('skills')  # Assume 'skills' is the name of your field in the form
        selected_skills_ids = [int(id) for id in selected_skills_ids if id.isdigit()]  # Convert IDs to integers
        
        new_skill_name = request.POST.get('new_skill', '').strip()  # Get new skill
        if new_skill_name:
            formatted_skill_name = new_skill_name.capitalize()

            new_skill, created = Skill.objects.get_or_create(name=formatted_skill_name)  # Create or get the new skill
            freelancer.skills.add(new_skill)  # Add new skill to the freelancer's profile
            request.session['show_add_modal'] = True
            return redirect('profile_settings_freelancer')


        if selected_skills_ids:
            freelancer.skills.set(selected_skills_ids)  # Update selected skills

        
        freelancer.save()  # Save changes to the freelancer's profile

    # Render profile settings page
    return render(request, 'Users/profileSettingsFreelancer.html', {
        'user': user,
        'freelancer': freelancer,
        'educations': educations,
        'certifications': certifications,
        'work_experiences': work_experiences,
        'portfolios': portfolios,
        'skills': skills,
        'freelancer_languages': languages,
        'all_languages': all_languages,  # Pass all languages for selection
        'all_skills': Skill.objects.all(), 
        'show_update_modal': show_update_modal,
        'show_add_modal': show_add_modal,
        'show_delete_modal': show_delete_modal,
        'countries': countries
    })


@login_required
def profile_settings_client(request):
    user = request.user  # Get the currently logged-in user
    try:
        client = ClientProfile.objects.get(user=user)
    except FreelancerProfile.DoesNotExist:
        # Create a new ClientProfile if it does not exist
        client = ClientProfile.objects.create(user=user)
    
    show_modal = False

    if request.method == 'POST':
        # Check which form is being submitted
        if 'update_user_info' in request.POST:
            # Update user info (first name, last name, email, username)
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.username = request.POST.get('username', user.username)
            user.save()  # Save updated user info

            # Update client profile info 
            client.company_name = request.POST.get('company_name', client.company_name)
            client.company_website = request.POST.get('company_website', client.company_website)
            client.phone = request.POST.get('phone', client.phone)
            client.city = request.POST.get('city', client.city)
            client.country = request.POST.get('country', client.country)
            client.address = request.POST.get('address', client.address)
            client.save()  # Save updated freelancer info

            show_modal = True

    # Render profile settings page
    return render(request, 'Users/profileSettingsClient.html', {
        'user': user,
        'client': client,
        'show_modal': show_modal,
        'countries': countries
    })
    
def search_freelancers(request):
    """
    View for searching freelancers based on a keyword and selected skills.

    This view handles both GET requests with search parameters and displays 
    the search form along with the filtered results.

    The filtering includes:
    - Username, first name, last name, or full name (concatenation of first and last names).
    - Skills, if any are selected from the form.

    Returns:
        Rendered template displaying the search form and list of freelancers.
    """

    # Copy the GET parameters to modify them
    filtered_get = request.GET.copy()

    # Remove the 'skills' parameter if it is empty
    if 'skills' in filtered_get and filtered_get['skills'] == '':
        del filtered_get['skills']

    # Initialize the search form with the filtered GET data
    form = FreelancerSearchForm(filtered_get or None)
    freelancers = FreelancerProfile.objects.all()

    print("GET request después de limpieza:", filtered_get)  # Debugging: log GET request after cleaning

    if form.is_valid():  # Check if the form is valid
        # Capture the value of the keyword field
        keyword = form.cleaned_data.get('keyword', '').strip()
        print("Keyword recibido:", keyword)  # Debugging: log the received keyword

        # Filter by username, first name, last name, or full name
        if keyword:
            # Annotate a virtual field that concatenates first_name and last_name
            freelancers = freelancers.annotate(
                full_name=Concat('user__first_name', Value(' '), 'user__last_name')
            ).filter(
                Q(user__username__icontains=keyword) | 
                Q(user__first_name__icontains=keyword) | 
                Q(user__last_name__icontains=keyword) |
                Q(full_name__icontains=keyword)  # Search by full name
            )
            print(f"Freelancers filtrados por keyword '{keyword}':", freelancers.count())  # Log the number of filtered freelancers

        # Filter by skills if any skills are selected
        skills = form.cleaned_data.get('skills')
        print("Skills recibidas:", skills)  # Debugging: log received skills
        if skills and skills.exists():
            freelancers = freelancers.filter(skills__in=skills).distinct()  # Filter by selected skills
            print(f"Freelancers filtrados por skills '{skills}':", freelancers.count())  # Log the count of filtered freelancers

    return render(request, 'Users/search_freelancers.html', {
        'form': form,
        'freelancers': freelancers  # Pass the filtered freelancers to the template
    })


def freelancer_profile(request, id):
    """
    View para mostrar el perfil de un freelancer, incluyendo comentarios y calificaciones.
    """
    freelancer = get_object_or_404(FreelancerProfile, user__id=id)
    
    # Calcular la calificación promedio
    average_rating = FreelancerComment.objects.filter(freelancer=freelancer).aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)
    
    # Calcular estrellas completas, medias y vacías para el promedio
    full_stars = int(average_rating)
    half_stars = 1 if (average_rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_stars
    
    # Manejar los comentarios
    if request.method == 'POST':
        form = FreelancerCommentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            rating = form.cleaned_data['rating']
            comment_content = form.cleaned_data['comment']
            
            try:
                user = User.objects.get(username=username)
                if user.email != email:
                    messages.error(request, _("El email no coincide con el username proporcionado."))
                else:
                    # Verificar si el usuario ya ha comentado
                    existing_comment = FreelancerComment.objects.filter(freelancer=freelancer, user=user).first()
                    if existing_comment:
                        messages.error(request, _("Ya has comentado a este freelancer."))
                    else:
                        # Crear y guardar el comentario
                        FreelancerComment.objects.create(
                            freelancer=freelancer,
                            user=user,
                            rating=rating,
                            comment=comment_content
                        )
                        messages.success(request, _("¡Gracias por tu comentario!"))
                        return redirect('freelancer_profile', id=freelancer.user.id)
            except User.DoesNotExist:
                messages.error(request, _("El username proporcionado no existe."))
        else:
            messages.error(request, _("Por favor, corrige los errores en el formulario."))
    else:
        form = FreelancerCommentForm()
    
    # Obtener todos los comentarios existentes ordenados por fecha de creación
    comments = FreelancerComment.objects.filter(freelancer=freelancer).order_by('-created_at')
    
    # Implementar Paginación: 5 comentarios por página
    paginator = Paginator(comments, 5)  # 5 comentarios por página
    page = request.GET.get('page')
    
    try:
        comments_paginated = paginator.page(page)
    except PageNotAnInteger:
        comments_paginated = paginator.page(1)
    except EmptyPage:
        comments_paginated = paginator.page(paginator.num_pages)
    
    # Calcular la calificación promedio (ya calculado arriba)
    
    context = {
        'freelancer': freelancer,
        'comments': comments_paginated,
        'form': form,
        'average_rating': average_rating,
        'full_stars': range(full_stars),
        'half_stars': range(half_stars),
        'empty_stars': range(empty_stars),
        'is_paginated': comments_paginated.has_other_pages(),
        'paginator': paginator,
        'page_obj': comments_paginated,
    }
    
    return render(request, 'Users/freelancer_profile.html', context)


def search_clients(request):
    """
    View for searching clients based on a keyword and country.

    This view processes the search form to filter clients by:
    - Company name, city, or country based on the keyword.
    - Specific country if selected.

    Returns:
        Rendered template displaying the search form and list of clients.
    """
    form = ClientSearchForm(request.GET or None)  # Initialize the search form with GET data
    clients = ClientProfile.objects.all()  # Start with all clients

    if form.is_valid():  # Check if the form is valid
        keyword = form.cleaned_data.get('keyword')  # Get the keyword
        country = form.cleaned_data.get('country')  # Get the selected country

        if keyword:  # Filter by keyword
            clients = clients.filter(
                Q(company_name__icontains=keyword) |
                Q(country__icontains=keyword)
            ).distinct()  # Remove duplicates

        if country:  # Filter by country
            clients = clients.filter(country=country)

    return render(request, 'Users/search_clients.html', {
        'form': form,
        'clients': clients  # Pass the filtered clients to the template
    })


def client_profile(request, id):
    """
    View for displaying a client's profile.

    This view retrieves the client's profile using the provided user ID 
    and renders the corresponding template.

    Args:
        id (int): The user ID of the client.

    Returns:
        Rendered template displaying the client's profile.
    """
    
    print(1)
    client = get_object_or_404(ClientProfile, id=id)  # Get the freelancer profile or 404
    print(client)

    return render(request, 'Users/client_profile.html', {'client': client})  # Render the profile template
