from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages  # Para los mensajes de error y éxito
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend 
from django.shortcuts import get_object_or_404
from .models import FreelancerProfile, Skill, Certification, WorkExperience, Portfolio
from django.db.models import Q, Value
from django.db.models.functions import Concat
from Projects.models import *
from Projects.models import Application



@never_cache
def freelancer_signup(request):
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Explicitly pass the backend
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('work_experience_register')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = FreelancerSignUpForm()

    return render(request, 'Users/freelancer_signup.html', {'form': form})

@never_cache
def client_signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
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
                auth_login(request, user)  # Iniciar sesión

                # Redirigir al 'next' si está en los parámetros, de lo contrario, al dashboard
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    if user.user_type == 'freelancer':
                        return redirect('home_freelancer')
                    elif user.user_type == 'client':
                        return redirect('home_client')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
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
        form = FreelancerSignUpForm(request.POST, request.FILES)  # Añadir request.FILES
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Usamos auth_login para evitar conflicto
            return redirect('work_experience_register')  # Redirige al registro de educación
    else:
        form = FreelancerSignUpForm()
    return render(request, 'Users/freelancer_signup.html', {'form': form})


def work_experience_register_view(request):
    freelancer = request.user.freelancer_profile
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
    freelancer = request.user.freelancer_profile
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
    freelancer = request.user.freelancer_profile
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
    freelancer = request.user.freelancer_profile
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
    freelancer = request.user.freelancer_profile
    if request.method == "POST":
        # Procesar habilidades predefinidas seleccionadas
        selected_skills_ids = request.POST.get('skills', '')
        if selected_skills_ids:
            selected_skills_ids = [int(id) for id in selected_skills_ids.split(',') if id.isdigit()]

        # Procesar nuevas habilidades ingresadas
        new_skills = request.POST.get('new_skills', '').split(',')

        # Actualizar habilidades seleccionadas
        if selected_skills_ids:
            freelancer.skills.set(selected_skills_ids)  # Actualiza las habilidades predefinidas

        # Agregar nuevas habilidades
        for skill_name in new_skills:
            skill_name = skill_name.strip()
            if skill_name:
                skill, created = Skill.objects.get_or_create(name=skill_name)
                freelancer.skills.add(skill)  # Agrega la nueva habilidad al perfil del freelancer

        freelancer.save()  # Guardar los cambios

        return redirect('home_freelancer')

    else:
        form = SkillsForm(instance=freelancer)
        form.fields['skills'].queryset = Skill.objects.all().order_by('name')[:10]  # Limitar a las primeras 8 habilidades
        return render(request, 'Users/register_skills.html', {'form': form})

@login_required
def register_languages_view(request):
    freelancer = request.user.freelancer_profile
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

def home_freelancer(request):
    freelancer_profile = request.user.freelancer_profile  # Obtener el perfil del freelancer
    # Obtener los contratos activos asociados a este freelancer
    active_contracts = Contract.objects.filter(freelancer=freelancer_profile, status='active')
    # Obtener los proyectos asociados a esos contratos
    projects = [contract.project for contract in active_contracts]
    total_projects = len(projects)  # Contar proyectos

    return render(request, 'Users/homeFreelancer.html', {
        'projects': projects,
        'total_projects': total_projects,

    })

def createProject(request):
    return render(request, 'Users/createProject.html')

def change_password(request):
    return render(request, 'Users/changePassword.html')

@login_required
def profile_settings(request):
    user = request.user
    try:
        freelancer = FreelancerProfile.objects.get(user=user)
        educations = freelancer.educations.all()
        certifications = Certification.objects.filter(freelancer=freelancer)
        work_experiences = WorkExperience.objects.filter(freelancer=freelancer)
        portfolios = Portfolio.objects.filter(freelancer=freelancer)
        skills = freelancer.skills.all()
    except FreelancerProfile.DoesNotExist:
        freelancer = FreelancerProfile.objects.create(user=user)
        educations = []
        certifications = []
        work_experiences = []
        portfolios = []
        skills = []

    if request.method == 'POST':
        # Verificar qué formulario se está enviando para procesar solo esa sección
        if 'update_user_info' in request.POST:
            # Actualizar los datos del usuario (nombre, email, etc.)
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.username = request.POST.get('username', user.username)
            user.save()  # Guarda los datos actualizados del usuario

            # Actualizar los datos del freelancer (teléfono, ciudad, país, etc.)
            freelancer.phone = request.POST.get('phone', freelancer.phone)
            freelancer.city = request.POST.get('city', freelancer.city)
            freelancer.country = request.POST.get('country', freelancer.country)
            freelancer.address = request.POST.get('address', freelancer.address)
            freelancer.save()  # Guarda los cambios del freelancer

            messages.success(request, "User information updated successfully.")
            return redirect('profile_settings')

        elif 'add_education' in request.POST:
            # Agregar nueva educación
            if request.POST.get('new_institution_name') and request.POST.get('new_degree_obtained'):
                new_education = Education(
                    freelancer=freelancer,
                    institution_name=request.POST.get('new_institution_name'),
                    degree_obtained=request.POST.get('new_degree_obtained'),
                    start_date=request.POST.get('new_start_date'),
                    end_date=request.POST.get('new_end_date'),
                    description=request.POST.get('new_description')
                )
                new_education.save()

        elif 'delete_education' in request.POST:
            # Eliminar educación
            education_id = request.POST.get('delete_education')
            try:
                education = Education.objects.get(id=education_id, freelancer=freelancer)
                education.delete()
                messages.success(request, 'Educational record deleted successfully.')
            except Education.DoesNotExist:
                messages.error(request, 'The education record could not be found.')
            return redirect('profile_settings')

        elif 'add_certification' in request.POST:
            # Agregar nueva certificación
            if request.POST.get('new_certification_name') and request.POST.get('new_issuing_organization'):
                new_certification = Certification(
                    freelancer=freelancer,
                    certification_name=request.POST.get('new_certification_name'),
                    issuing_organization=request.POST.get('new_issuing_organization'),
                    issue_date=request.POST.get('new_issue_date'),
                    expiration_date=request.POST.get('new_expiration_date'),
                    short_description=request.POST.get('new_certification_description')
                )
                new_certification.save()

        elif 'delete_certification' in request.POST:
            # Eliminar certificación
            certification_id = request.POST.get('delete_certification')
            try:
                certification = Certification.objects.get(id=certification_id, freelancer=freelancer)
                certification.delete()
                messages.success(request, 'Certification deleted successfully.')
            except Certification.DoesNotExist:
                messages.error(request, 'The certification could not be found.')
            return redirect('profile_settings')

        elif 'add_experience' in request.POST:
            # Agregar nueva experiencia laboral
            if request.POST.get('new_company_name') and request.POST.get('new_position'):
                new_experience = WorkExperience(
                    freelancer=freelancer,
                    company_name=request.POST.get('new_company_name'),
                    position=request.POST.get('new_position'),
                    start_date=request.POST.get('new_experience_start_date'),
                    end_date=request.POST.get('new_experience_end_date'),
                    description=request.POST.get('new_experience_description')
                )
                new_experience.save()

        elif 'delete_experience' in request.POST:
            # Eliminar experiencia laboral
            experience_id = request.POST.get('delete_experience')
            try:
                experience = WorkExperience.objects.get(id=experience_id, freelancer=freelancer)
                experience.delete()
                messages.success(request, 'Work experience deleted successfully.')
            except WorkExperience.DoesNotExist:
                messages.error(request, 'The work experience could not be found.')
            return redirect('profile_settings')

        elif 'add_portfolio' in request.POST:
            # Agregar nuevo portafolio
            if request.POST.get('new_portfolio_url') and request.POST.get('new_portfolio_description'):
                new_portfolio = Portfolio(
                    freelancer=freelancer,
                    url=request.POST.get('new_portfolio_url'),
                    description=request.POST.get('new_portfolio_description')
                )
                new_portfolio.save()

        elif 'delete_portfolio' in request.POST:
            # Eliminar portafolio
            portfolio_id = request.POST.get('delete_portfolio')
            try:
                portfolio = Portfolio.objects.get(id=portfolio_id, freelancer=freelancer)
                portfolio.delete()
                messages.success(request, 'Portfolio entry deleted successfully.')
            except Portfolio.DoesNotExist:
                messages.error(request, 'The portfolio entry could not be found.')
            return redirect('profile_settings')
        
        selected_skills_ids = request.POST.getlist('skills')  # Asume que 'skills' es el nombre de tu campo en el formulario
        selected_skills_ids = [int(id) for id in selected_skills_ids if id.isdigit()]  # Convierte los IDs a enteros
        
        new_skill_name = request.POST.get('new_skill', '').strip()
        if new_skill_name:
            new_skill, created = Skill.objects.get_or_create(name=new_skill_name)
            freelancer.skills.add(new_skill)  # Agrega la nueva habilidad al perfil del freelancer

        if selected_skills_ids:
            freelancer.skills.set(selected_skills_ids)  # Actualiza las habilidades seleccionadas

        freelancer.save()  # Guarda los cambios del freelancer
        return redirect('profile_settings')

    return render(request, 'Users/profileSettings.html', {
        'user': user,
        'freelancer': freelancer,
        'educations': educations,
        'certifications': certifications,
        'work_experiences': work_experiences,
        'portfolios': portfolios,
        'skills': skills,
        'all_skills': Skill.objects.all()
    })


def search_freelancers(request):
    form = FreelancerSearchForm(request.GET or None)
    freelancers = FreelancerProfile.objects.all()

    print("GET request:", request.GET)

    if form.is_valid():
        # Capturar el valor del campo keyword
        keyword = form.cleaned_data.get('keyword', '').strip()
        print("Keyword recibido:", keyword)

        # Filtrar por username, first_name, last_name o nombre completo
        if keyword:
            # Anotar un campo virtual que concatene first_name y last_name
            freelancers = freelancers.annotate(
                full_name=Concat('user__first_name', Value(' '), 'user__last_name')
            ).filter(
                Q(user__username__icontains=keyword) | 
                Q(user__first_name__icontains=keyword) | 
                Q(user__last_name__icontains=keyword) |
                Q(full_name__icontains=keyword)  # Búsqueda por nombre completo
            )
            print(f"Freelancers filtrados por keyword '{keyword}':", freelancers.count())

        # Filtrar por skills si hay habilidades seleccionadas
        skills = form.cleaned_data.get('skills')
        print("Skills recibidas:", skills)
        if skills and skills.exists():
            freelancers = freelancers.filter(skills__in=skills).distinct()
            print(f"Freelancers filtrados por skills '{skills}':", freelancers.count())

    return render(request, 'Users/search_freelancers.html', {
        'form': form,
        'freelancers': freelancers
    })


def freelancer_profile(request, id):
    freelancer = get_object_or_404(FreelancerProfile, user__id=id)
    return render(request, 'Users/freelancer_profile.html', {'freelancer': freelancer})



def search_clients(request):
    form = ClientSearchForm(request.GET or None)
    clients = ClientProfile.objects.all()

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        country = form.cleaned_data.get('country')

        if keyword:
            clients = clients.filter(
                Q(company_name__icontains=keyword) |
                Q(city__icontains=keyword) |
                Q(country__icontains=keyword)
            ).distinct()

        if country:
            clients = clients.filter(country=country)

    return render(request, 'Users/search_clients.html', {
        'form': form,
        'clients': clients
    })
    
    


def client_profile(request, id):
    client = get_object_or_404(ClientProfile, user__id=id)
    return render(request, 'Users/clientProfile.html', {'client': client})
    

