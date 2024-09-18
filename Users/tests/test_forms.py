import pytest
from Users.models import User, FreelancerProfile, Skill, Education, WorkExperience, Certification, Portfolio, ClientProfile
from Users.forms import FreelancerSignUpForm, ClientSignUpForm, WorkExperienceFormSet, CertificationFormSet, EducationFormSet, PortfolioFormSet
from django.test import Client

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword', user_type='freelancer')

@pytest.fixture
def freelancer_profile(user):
    # Crear un perfil de freelancer asociado al usuario
    return FreelancerProfile.objects.create(
        user=user,
        country='US',
        city='New York',
        phone='1234567890',
        address='1234 Freelance Ave'
    )

@pytest.mark.django_db
def test_freelancer_signup_form_valid():
    # Datos simulados para el formulario
    data = {
        'username': 'testfreelancer',
        'email': 'testfreelancer@example.com',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Freelance Ave'
    }

    form = FreelancerSignUpForm(data=data)
    
    # Verificar que el formulario sea válido
    assert form.is_valid(), form.errors
    
    # Guardar el formulario para crear el usuario y perfil de freelancer
    user = form.save()

    # Verificar que el usuario y el perfil de freelancer se han creado correctamente
    assert User.objects.filter(username='testfreelancer').exists()
    assert FreelancerProfile.objects.filter(user=user).exists()
    assert FreelancerProfile.objects.get(user=user).city == 'New York'

@pytest.mark.django_db
def test_freelancer_signup_form_invalid_password_mismatch():
    # Datos simulados con contraseñas que no coinciden
    data = {
        'username': 'testfreelancer',
        'email': 'testfreelancer@example.com',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'password1': 'testpassword123',
        'password2': 'wrongpassword',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Freelance Ave'
    }

    form = FreelancerSignUpForm(data=data)
    
    # Verificar que el formulario no sea válido debido a las contraseñas que no coinciden
    assert not form.is_valid()
    assert 'password2' in form.errors

@pytest.mark.django_db
def test_client_signup_form_valid():
    # Datos simulados para el formulario
    data = {
        'username': 'testclient',
        'email': 'testclient@example.com',
        'first_name': 'Test',
        'last_name': 'Client',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Client Ave',
        'company_name': 'Test Company',
        'company_website': 'http://example.com'
    }

    form = ClientSignUpForm(data=data)
    
    # Verificar que el formulario sea válido
    assert form.is_valid(), form.errors
    
    # Guardar el formulario para crear el usuario y perfil de cliente
    user = form.save()

    # Verificar que el usuario y el perfil de cliente se han creado correctamente
    assert User.objects.filter(username='testclient').exists()
    assert ClientProfile.objects.filter(user=user).exists()
    assert ClientProfile.objects.get(user=user).company_name == 'Test Company'

@pytest.mark.django_db
def test_client_signup_form_invalid_missing_company_name():
    # Datos simulados pero sin el campo requerido 'company_name'
    data = {
        'username': 'testclient',
        'email': 'testclient@example.com',
        'first_name': 'Test',
        'last_name': 'Client',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Client Ave',
        'company_website': 'http://example.com'
    }

    form = ClientSignUpForm(data=data)
    
    # Verificar que el formulario no sea válido debido a la falta de 'company_name'
    assert not form.is_valid()
    assert 'company_name' in form.errors

@pytest.mark.django_db
def test_work_experience_formset_valid(freelancer_profile):
    data = {
        'workexperience_set-TOTAL_FORMS': '1',
        'workexperience_set-INITIAL_FORMS': '0',
        'workexperience_set-MIN_NUM_FORMS': '0',
        'workexperience_set-MAX_NUM_FORMS': '1000',
        'workexperience_set-0-company_name': 'Company A',
        'workexperience_set-0-position': 'Developer',
        'workexperience_set-0-start_date': '2020-01-01',
        'workexperience_set-0-end_date': '2021-01-01',
        'workexperience_set-0-description': 'Developed cool stuff'
    }

    formset = WorkExperienceFormSet(data, instance=freelancer_profile)

    if not formset.is_valid():
        print(formset.errors)
    assert formset.is_valid()


@pytest.mark.django_db
def test_education_formset_valid(freelancer_profile):
    data = {
        'education_set-TOTAL_FORMS': '1',
        'education_set-INITIAL_FORMS': '0',
        'education_set-MIN_NUM_FORMS': '0',
        'education_set-MAX_NUM_FORMS': '1000',
        'education_set-0-school_name': 'University A',
        'education_set-0-degree': 'BSc Computer Science',
        'education_set-0-start_date': '2016-01-01',
        'education_set-0-end_date': '2020-01-01',
        'education_set-0-description': 'Studied Computer Science'
    }

    formset = EducationFormSet(data, instance=freelancer_profile)

    if not formset.is_valid():
        print(formset.errors)  # Imprimir los errores si el formset no es válido
    assert formset.is_valid()

@pytest.mark.django_db
def test_certification_formset_valid(freelancer_profile):
    data = {
        'certification_set-TOTAL_FORMS': '1',
        'certification_set-INITIAL_FORMS': '0',
        'certification_set-MIN_NUM_FORMS': '0',
        'certification_set-MAX_NUM_FORMS': '1000',
        'certification_set-0-title': 'Certification A',
        'certification_set-0-organization': 'Certifying Body',
        'certification_set-0-date_awarded': '2021-01-01'
    }

    formset = CertificationFormSet(data, instance=freelancer_profile)

    assert formset.is_valid()

@pytest.mark.django_db
def test_portfolio_formset_valid(freelancer_profile):
    data = {
        'portfolio_set-TOTAL_FORMS': '1',
        'portfolio_set-INITIAL_FORMS': '0',
        'portfolio_set-MIN_NUM_FORMS': '0',
        'portfolio_set-MAX_NUM_FORMS': '1000',
        'portfolio_set-0-title': 'Project A',
        'portfolio_set-0-description': 'Developed a project',
        'portfolio_set-0-url': 'http://example.com'
    }

    formset = PortfolioFormSet(data, instance=freelancer_profile)

    assert formset.is_valid()




##########
#Not valid cases
##########



@pytest.mark.django_db
def test_freelancer_signup_form_invalid_missing_username():
    # Datos simulados sin el campo requerido 'username'
    data = {
        'email': 'testfreelancer@example.com',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Freelance Ave'
    }

    form = FreelancerSignUpForm(data=data)
    
    # Verificar que el formulario no sea válido debido a la falta de 'username'
    assert not form.is_valid()
    assert 'username' in form.errors


@pytest.mark.django_db
def test_freelancer_signup_form_invalid_email_format():
    # Datos simulados con un formato de correo inválido
    data = {
        'username': 'testfreelancer',
        'email': 'invalidemail',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Freelance Ave'
    }

    form = FreelancerSignUpForm(data=data)
    
    # Verificar que el formulario no sea válido debido al formato incorrecto del correo
    assert not form.is_valid()
    assert 'email' in form.errors

@pytest.mark.django_db
def test_freelancer_signup_form_invalid_short_password():
    # Datos simulados con una contraseña demasiado corta
    data = {
        'username': 'testfreelancer',
        'email': 'testfreelancer@example.com',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'password1': 'short',
        'password2': 'short',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Freelance Ave'
    }

    form = FreelancerSignUpForm(data=data)
    
    # Verificar que el formulario no sea válido debido a la contraseña demasiado corta
    assert not form.is_valid()
    assert 'password2' in form.errors

@pytest.mark.django_db
def test_client_signup_form_invalid_website_format():
    # Datos simulados con una URL de empresa no válida
    data = {
        'username': 'testclient',
        'email': 'testclient@example.com',
        'first_name': 'Test',
        'last_name': 'Client',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Client Ave',
        'company_name': 'Test Company',
        'company_website': 'invalidurl'
    }

    form = ClientSignUpForm(data=data)
    
    # Verificar que el formulario no sea válido debido al formato incorrecto de la URL
    assert not form.is_valid()
    assert 'company_website' in form.errors

def test_work_experience_formset_missing_required_fields():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': '2024-09-10',
        'form-0-end_date': '2024-09-20',
        'form-0-company': '',  # Campo obligatorio vacío
        'form-0-position': '',  # Campo obligatorio vacío
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'company' in formset.forms[0].errors  # Verificar que hay un error en el campo `company`
    assert 'position' in formset.forms[0].errors  # Verificar que hay un error en el campo `position`

@pytest.mark.django_db
def test_work_experience_formset_missing_required_fields(freelancer_profile):
    # Datos simulados faltando campos requeridos
    data = {
        'workexperience_set-TOTAL_FORMS': '1',
        'workexperience_set-INITIAL_FORMS': '0',
        'workexperience_set-MIN_NUM_FORMS': '0',
        'workexperience_set-MAX_NUM_FORMS': '1000',
        'workexperience_set-0-company_name': '',  # Campo requerido faltante
        'workexperience_set-0-position': 'Developer',
        'workexperience_set-0-start_date': '2020-01-01',
        'workexperience_set-0-end_date': '2021-01-01',
        'workexperience_set-0-description': 'Developed cool stuff'
    }

    formset = WorkExperienceFormSet(data, instance=freelancer_profile)

    # Verificar que el formulario no sea válido debido a los campos faltantes
    assert not formset.is_valid()
    assert 'company_name' in formset.forms[0].errors  # Verifica que hay un error en el campo 'company_name'