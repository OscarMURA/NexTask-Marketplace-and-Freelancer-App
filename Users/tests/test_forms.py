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

    # Datos del formset incluyendo ManagementForm
    formset_data = {
        'work_experiences-0-company_name': 'Company A',
        'work_experiences-0-position': 'Developer',
        'work_experiences-0-start_date': '2020-01-01',
        'work_experiences-0-end_date': '2022-01-01',
        'work_experiences-0-description': 'Developed software',
        'work_experiences-TOTAL_FORMS': '1',         # Número total de formularios
        'work_experiences-INITIAL_FORMS': '0',       # Número de formularios iniciales (cero porque estamos creando uno nuevo)
        'work_experiences-MIN_NUM_FORMS': '0',       # Mínimo de formularios (opcional, puede ser 0)
        'work_experiences-MAX_NUM_FORMS': '1000',    # Máximo de formularios
    }

    # Crear el formset con los datos de prueba
    formset = WorkExperienceFormSet(data=formset_data, instance=profile)

    # Verificar que el formset sea válido
    assert formset.is_valid(), f"Formset errors: {formset.errors}, non_form_errors: {formset.non_form_errors()}"


@pytest.mark.django_db
def test_education_formset_valid():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)

    # Datos del formset incluyendo ManagementForm
    formset_data = {
        'educations-0-institution_name': 'University A',
        'educations-0-degree_obtained': 'Bachelor',
        'educations-0-start_date': '2015-09-01',
        'educations-0-end_date': '2019-06-01',
        'educations-TOTAL_FORMS': '1',        # Número total de formularios
        'educations-INITIAL_FORMS': '0',      # Número de formularios iniciales (cero porque estamos creando uno nuevo)
        'educations-MIN_NUM_FORMS': '0',      # Mínimo de formularios (opcional, puede ser 0)
        'educations-MAX_NUM_FORMS': '1000'    # Máximo de formularios
    }

    # Crear el formset con los datos de prueba
    formset = EducationFormSet(data=formset_data, instance=profile)

    # Verificar que el formset sea válido
    assert formset.is_valid(), formset.errors  # Muestra los errores si no es válido

import pytest
from Users.forms import CertificationFormSet
from Users.models import User, FreelancerProfile

@pytest.mark.django_db
def test_certification_formset():
    # Crear un usuario de prueba
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)

    # Datos para el formset con el prefijo adecuado
    formset_data = {
        'certification_set-0-certification_name': 'Certification 1',
        'certification_set-0-issuing_organization': 'Organization A',
        'certification_set-0-issue_date': '2023-01-01',
        'certification_set-0-expiration_date': '2024-01-01',
        'certification_set-0-short_description': 'Description A',
        'certification_set-TOTAL_FORMS': '1',
        'certification_set-INITIAL_FORMS': '0',
        'certification_set-MAX_NUM_FORMS': '1000'  # Este campo es requerido por Django
    }

    # Crear el formset con los datos de prueba
    formset = CertificationFormSet(data=formset_data, instance=profile)

    # Si el formset no es válido, imprimir los errores para depurar
    if not formset.is_valid():
        for form in formset:
            print(f"Form errors: {form.errors}")
        print(f"Non-form errors: {formset.non_form_errors()}")

    # Asegurarnos de que el formset sea válido
    assert formset.is_valid(), f"Formset errors: {formset.errors}, non_form_errors: {formset.non_form_errors()}"


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
        'work_experiences-TOTAL_FORMS': '1',  # Cambiar el prefijo a 'work_experiences'
        'work_experiences-INITIAL_FORMS': '0',
        'work_experiences-MIN_NUM_FORMS': '0',
        'work_experiences-MAX_NUM_FORMS': '1000',
        'work_experiences-0-company_name': '',  # Campo faltante (para probar la validación)
        'work_experiences-0-position': 'Developer',
        'work_experiences-0-start_date': '2020-01-01',
        'work_experiences-0-end_date': '2022-01-01',
        'work_experiences-0-description': 'Developed software',
    }

    formset = WorkExperienceFormSet(data=formset_data, instance=profile)

    # Depuración de errores si el formset no es válido
    if not formset.is_valid():
        for form in formset:
            print(f"Form errors: {form.errors}")
        print(f"Non-form errors: {formset.non_form_errors()}")
        print(f"ManagementForm data: {formset.management_form}")

    # Verificación de la cantidad de formularios
    assert len(formset.forms) > 0, "No forms found in formset"

    # Verificar que el formset no sea válido
    assert not formset.is_valid()

    # Verificar que 'company_name' tenga el error correspondiente
    assert 'company_name' in formset.forms[0].errors, "No error found for 'company_name' field"

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
    assert response.url == reverse('work_experience_register')  # Expected redirect URL


@pytest.mark.django_db
def test_freelancer_signup_form_invalid_long_username():
    data = {
        'username': 'a' * 256,  # Excede el límite de longitud
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

    form = FreelancerSignUpForm(data=data)
    assert not form.is_valid()
    assert 'username' in form.errors


@pytest.mark.django_db
def test_client_signup_form_valid_url():
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
        'company_website': 'https://example.com'  # URL válida con https
    }

    form = ClientSignUpForm(data=data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_freelancer_signup_form_optional_fields():
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
        'country': 'US',
        'city': 'New York',
        # Dejar opcionales vacíos
        'phone': '',
        'address': ''
    }

    form = FreelancerSignUpForm(data=data)
    assert form.is_valid()
"""""""""
@pytest.mark.django_db
def test_work_experience_formset_delete_entry():
    # Crear un usuario y un perfil de freelancer asociado
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)

    # Crear una experiencia laboral asociada al freelancer
    work_experience = WorkExperience.objects.create(
        freelancer=profile,
        company_name='Company A',
        position='Developer',
        start_date='2020-01-01',
        end_date='2022-01-01',
        description='Developed software'
    )

    # Datos del formset que marcarán la experiencia laboral para eliminarse
    formset_data = {
        'workexperience_set-0-id': work_experience.id,  # Usar el id directamente
        'workexperience_set-0-company_name': 'Company A',
        'workexperience_set-0-position': 'Developer',
        'workexperience_set-0-start_date': '2020-01-01',
        'workexperience_set-0-end_date': '2022-01-01',
        'workexperience_set-0-description': 'Developed software',
        'workexperience_set-0-DELETE': 'on',  # Marcado para eliminar
        'workexperience_set-TOTAL_FORMS': '1',  # Total de formularios
        'workexperience_set-INITIAL_FORMS': '1',  # Formularios ya inicializados
        'workexperience_set-MAX_NUM_FORMS': '1000',  # Puedes ajustar esto
    }

    # Crear el formset con los datos y el perfil de freelancer
    formset = WorkExperienceFormSet(data=formset_data, instance=profile)

    # Verificamos que el formset sea válido
    assert formset.is_valid(), formset.errors  # Imprime errores si no es válido
"""

@pytest.mark.django_db
def test_work_experience_formset_invalid_date_range():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)

    formset_data = {
        'form-0-company_name': 'Company A',
        'form-0-position': 'Developer',
        'form-0-start_date': '2022-01-01',
        'form-0-end_date': '2020-01-01',  # Fecha de finalización anterior a la fecha de inicio
        'form-0-description': 'Developed software',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }

    formset = WorkExperienceFormSet(data=formset_data, instance=profile)
    
    assert not formset.is_valid()  # Debe ser False si hay errores

    print("Errores después de validar:", formset.errors)  # Ver errores después de validars

@pytest.mark.django_db
def test_portfolio_formset_invalid_url():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)

    formset_data = {
        'form-0-url': 'invalid-url',  # URL inválida
        'form-0-description': 'This is a project',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }

    formset = PortfolioFormSet(data=formset_data, instance=profile)
    assert not formset.is_valid()

@pytest.mark.django_db
def test_freelancer_profile_with_skills():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    skill1 = Skill.objects.create(name="Python")
    skill2 = Skill.objects.create(name="Django")
    
    # Asignar habilidades al perfil de freelancer
    profile.skills.add(skill1, skill2)
    
    # Verificar que las habilidades fueron correctamente asociadas
    assert profile.skills.filter(name="Python").exists()
    assert profile.skills.filter(name="Django").exists()

@pytest.mark.django_db
def test_client_signup_form_optional_website():
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
        'company_website': ''  # No proporcionar URL
    }

    form = ClientSignUpForm(data=data)
    assert form.is_valid(), form.errors
    user = form.save()

    # Verificar que el perfil de cliente se ha creado correctamente
    client_profile = ClientProfile.objects.get(user=user)
    assert client_profile.company_name == 'Test Company'
    assert client_profile.company_website == ''  # No hay URL

@pytest.mark.django_db
def test_skill_unique_constraint():
    skill1 = Skill.objects.create(name="Python")
    with pytest.raises(Exception):
        # Intentar crear una habilidad con el mismo nombre debería fallar
        Skill.objects.create(name="Python")

