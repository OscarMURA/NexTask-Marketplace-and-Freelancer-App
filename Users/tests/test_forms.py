import pytest
from Users.models import User, FreelancerProfile, Skill, Education, WorkExperience, Certification, Portfolio, ClientProfile
from Users.forms import FreelancerSignUpForm, ClientSignUpForm, WorkExperienceFormSet, CertificationFormSet, EducationFormSet, PortfolioFormSet
from django.test import Client
from django.urls import reverse

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
def test_work_experience_formset_valid():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    formset_data = {
        'form-0-company_name': 'Company A',
        'form-0-position': 'Developer',
        'form-0-start_date': '2020-01-01',
        'form-0-end_date': '2022-01-01',
        'form-0-description': 'Developed software',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }
    
    formset = WorkExperienceFormSet(data=formset_data, instance=profile)
    assert formset.is_valid()
    formset.save()
    assert WorkExperience.objects.filter(company_name='Company A').exists()

@pytest.mark.django_db
def test_education_formset_valid():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    formset_data = {
        'form-0-institution': 'University A',
        'form-0-degree': 'Bachelor',
        'form-0-start_date': '2015-09-01',
        'form-0-end_date': '2019-06-01',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }
    
    formset = EducationFormSet(data=formset_data, instance=profile)
    assert formset.is_valid()
    formset.save()
    assert Education.objects.filter(institution='University A').exists()

@pytest.mark.django_db
def test_certification_formset():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    formset_data = {
        'form-0-certification_name': 'Certification A',
        'form-0-issuing_organization': 'Organization A',
        'form-0-issue_date': '2022-01-01',
        'form-0-expiration_date': '2025-01-01',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }
    
    formset = CertificationFormSet(data=formset_data, instance=profile)
    assert formset.is_valid()
    formset.save()
    assert Certification.objects.filter(certification_name='Certification A').exists()


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
def test_freelancer_signup_form_invalid_missing_field():
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
        # Missing 'country' field
    }
    form = FreelancerSignUpForm(data=form_data)
    assert not form.is_valid()
    assert 'country' in form.errors

@pytest.mark.django_db
def test_client_signup_form_invalid_email():
    form_data = {
        'username': 'testclient',
        'email': 'invalid-email',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'password1': 'anotherpassword123',
        'password2': 'anotherpassword123',
        'country': 'US',
        'city': 'San Francisco',
        'phone': '9876543210',
        'address': '5678 Client Ave',
        'company_name': 'Tech Co.',
        'company_website': 'http://techco.com'
    }
    form = ClientSignUpForm(data=form_data)
    assert not form.is_valid()
    assert 'email' in form.errors

@pytest.mark.django_db
def test_freelancer_sign_up_saves_data():
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Test St.'
    }
    form = FreelancerSignUpForm(data=form_data)
    assert form.is_valid()
    user = form.save()
    assert User.objects.filter(username='testuser').exists()
    freelancer_profile = FreelancerProfile.objects.get(user=user)
    assert freelancer_profile.city == 'New York'

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

@pytest.mark.django_db
def test_work_experience_formset_missing_required_fields():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    formset_data = {
        'form-0-company_name': '',  # Missing required field
        'form-0-position': 'Developer',
        'form-0-start_date': '2020-01-01',
        'form-0-end_date': '2022-01-01',
        'form-0-description': 'Developed software',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }
    
    formset = WorkExperienceFormSet(data=formset_data, instance=profile)
    assert not formset.is_valid()
    assert 'company_name' in formset.errors[0]  # Check for specific field errors

@pytest.mark.django_db
def test_certification_formset():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    formset_data = {
        'form-0-certification_name': 'Certification 1',
        'form-0-issuing_organization': 'Organization A',
        'form-0-issue_date': '2023-01-01',
        'form-0-expiration_date': '2024-01-01',
        'form-0-short_description': 'Description A',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }
    
    formset = CertificationFormSet(data=formset_data, instance=profile)
    assert formset.is_valid()
    formset.save()
    assert Certification.objects.filter(certification_name='Certification 1').exists()

@pytest.mark.django_db
def test_freelancer_signup_redirect():
    client = Client()
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Test St.'
    }
    response = client.post(reverse('register_freelancer'), data=form_data)
    assert response.status_code == 302  # Redirection status code
    assert response.url == reverse('home_freelancer')  # Expected redirect URL

@pytest.mark.django_db
def test_freelancer_signup_with_certification_formset():
    client = Client()
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Test St.'
    }
    formset_data = {
        'form-0-certification_name': 'Certification A',
        'form-0-issuing_organization': 'Organization A',
        'form-0-issue_date': '2023-01-01',
        'form-0-expiration_date': '2024-01-01',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }
    
    response = client.post(reverse('register_freelancer'), data={**form_data, **formset_data})
    assert response.status_code == 302
    user = User.objects.get(username='testuser')
    assert Certification.objects.filter(certification_name='Certification A').exists()