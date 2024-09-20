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
        'form-0-company_name': '',
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
    assert 'company_name' in formset.errors[0]  # Debería retornar un error

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
    assert response.url == reverse('work_experience_register')  # Expected redirect URL

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
def test_freelancer_signup_form_invalid_phone_number():
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
        'country': 'US',
        'city': 'New York',
        'phone': 'invalid-phone',  # Número no válido
        'address': '1234 Test St.'
    }

    form = FreelancerSignUpForm(data=data)
    assert not form.is_valid()
    assert 'phone' in form.errors

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

@pytest.mark.django_db
def test_work_experience_formset_delete_entry():

    #Si se puede eliminar una experiencia laboral

    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    work_experience = WorkExperience.objects.create(
        freelancer=profile,  # Cambiado a 'freelancer'
        company_name='Company A',
        position='Developer',
        start_date='2020-01-01',
        end_date='2022-01-01',
        description='Developed software'
    )
    
    formset_data = {
        'form-0-id': str(work_experience.id),
        'form-0-company_name': 'Company A',
        'form-0-position': 'Developer',
        'form-0-start_date': '2020-01-01',
        'form-0-end_date': '2022-01-01',
        'form-0-description': 'Developed software',
        'form-0-DELETE': 'on',  # Marca para eliminar
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '1',
        'form-MAX_NUM_FORMS': ''
    }
    
    formset = WorkExperienceFormSet(data=formset_data, instance=profile)
    assert formset.is_valid()
    formset.save()

    # Verifica que la experiencia laboral haya sido eliminada
    assert not WorkExperience.objects.filter(id=work_experience.id).exists()

@pytest.mark.django_db
def test_education_formset_missing_required_fields():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    formset_data = {
        'form-0-institution_name': '',  # Falta nombre de institución
        'form-0-degree_obtained': 'Bachelor',
        'form-0-start_date': '2015-09-01',
        'form-0-end_date': '2019-06-01',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }

    formset = EducationFormSet(data=formset_data, instance=profile)
    assert not formset.is_valid()
    assert 'institution_name' in formset.errors[0]  # Verificar que el campo requerido tiene un error

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
    assert not formset.is_valid()
    assert 'end_date' in formset.errors[0]  # Verifica que haya un error de validación de fechas

@pytest.mark.django_db
def test_certification_formset_multiple_entries():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)

    formset_data = {
        'form-0-certification_name': 'Certification A',
        'form-0-issuing_organization': 'Organization A',
        'form-0-issue_date': '2022-01-01',
        'form-0-expiration_date': '2025-01-01',
        'form-1-certification_name': 'Certification B',
        'form-1-issuing_organization': 'Organization B',
        'form-1-issue_date': '2023-01-01',
        'form-1-expiration_date': '2026-01-01',
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }

    formset = CertificationFormSet(data=formset_data, instance=profile)
    assert formset.is_valid()
    formset.save()

    # Verifica que las dos certificaciones fueron creadas
    assert Certification.objects.filter(certification_name='Certification A').exists()
    assert Certification.objects.filter(certification_name='Certification B').exists()

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
    assert 'url' in formset.errors[0]  # Verifica que el error esté en el campo de URL

@pytest.mark.django_db
def test_work_experience_formset_delete_entry():
    # Crear un usuario y un perfil de freelancer asociado
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    # Crear una experiencia laboral asociada al freelancer
    work_experience = WorkExperience.objects.create(
        freelancer=profile,  # Usamos 'freelancer' ya que ese es el campo relacionado
        company_name='Company A',
        position='Developer',
        start_date='2020-01-01',
        end_date='2022-01-01',
        description='Developed software'
    )
    
    # Datos del formset que marcarán la experiencia laboral para eliminarse
    formset_data = {
        'form-0-id': str(work_experience.id),
        'form-0-company_name': 'Company A',
        'form-0-position': 'Developer',
        'form-0-start_date': '2020-01-01',
        'form-0-end_date': '2022-01-01',
        'form-0-description': 'Developed software',
        'form-0-DELETE': 'on',  # Marcado para eliminar
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '1',
        'form-MAX_NUM_FORMS': ''
    }
    
    # Crear el formset con los datos y el perfil de freelancer
    formset = WorkExperienceFormSet(data=formset_data, instance=profile)
    
    # Verificamos que el formset sea válido (debe validar que la eliminación es permitida)
    assert formset.is_valid()
    
    # Guardamos los cambios, lo que debería eliminar la entrada de experiencia laboral
    formset.save()

    # Verificamos que la experiencia laboral haya sido eliminada de la base de datos
    assert not WorkExperience.objects.filter(id=work_experience.id).exists()

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
def test_education_formset_update_entry():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    education = Education.objects.create(
        freelancer=profile,
        institution_name="University A",
        degree_obtained="Bachelor",
        start_date="2015-09-01",
        end_date="2019-06-01",
        description="Graduated with honors"
    )

    formset_data = {
        'form-0-id': str(education.id),
        'form-0-institution_name': 'University B',  # Actualizado
        'form-0-degree_obtained': 'Master',
        'form-0-start_date': '2020-01-01',
        'form-0-end_date': '2023-01-01',
        'form-0-description': 'Graduated with distinction',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '1',
        'form-MAX_NUM_FORMS': ''
    }

    # Crear el formset y verificar si es válido
    formset = EducationFormSet(data=formset_data, instance=profile)
    assert formset.is_valid(), formset.errors  # Depurar los errores si no es válido
    
    # Guardamos el formset
    formset.save()

    # Refrescar la instancia de Education desde la base de datos
    education.refresh_from_db()
    
    # Depurar el estado actual de la instancia
    print(f"Institution: {education.institution_name}")
    print(f"Degree: {education.degree_obtained}")
    
    # Verificar que los datos se hayan actualizado correctamente
    assert education.institution_name == 'University B', f"Institution was {education.institution_name}, expected 'University B'"
    assert education.degree_obtained == 'Master', f"Degree was {education.degree_obtained}, expected 'Master'"

@pytest.mark.django_db
def test_certification_formset_delete_multiple_entries():
    user = User.objects.create_user(username='testuser', password='securepassword123')
    profile = FreelancerProfile.objects.create(user=user)
    
    cert1 = Certification.objects.create(
        freelancer=profile,
        certification_name='Certification A',
        issuing_organization='Org A',
        issue_date='2020-01-01',
        expiration_date='2023-01-01'
    )
    cert2 = Certification.objects.create(
        freelancer=profile,
        certification_name='Certification B',
        issuing_organization='Org B',
        issue_date='2021-01-01',
        expiration_date='2024-01-01'
    )

    formset_data = {
        'form-0-id': str(cert1.id),
        'form-0-certification_name': 'Certification A',
        'form-0-issuing_organization': 'Org A',
        'form-0-issue_date': '2020-01-01',
        'form-0-expiration_date': '2023-01-01',
        'form-0-DELETE': 'on',  # Eliminar esta certificación
        'form-1-id': str(cert2.id),
        'form-1-certification_name': 'Certification B',
        'form-1-issuing_organization': 'Org B',
        'form-1-issue_date': '2021-01-01',
        'form-1-expiration_date': '2024-01-01',
        'form-1-DELETE': 'on',  # Eliminar esta certificación
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '2',
        'form-MAX_NUM_FORMS': ''
    }

    formset = CertificationFormSet(data=formset_data, instance=profile)
    assert formset.is_valid()
    formset.save()

    # Verificar que ambas certificaciones han sido eliminadas
    assert not Certification.objects.filter(certification_name='Certification A').exists()
    assert not Certification.objects.filter(certification_name='Certification B').exists()

@pytest.mark.django_db
def test_skill_unique_constraint():
    skill1 = Skill.objects.create(name="Python")
    with pytest.raises(Exception):
        # Intentar crear una habilidad con el mismo nombre debería fallar
        Skill.objects.create(name="Python")

