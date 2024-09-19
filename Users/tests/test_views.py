# myapp/tests/test_views.py
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from Users.forms import WorkExperienceFormSet
from Users.models import FreelancerProfile

User = get_user_model()

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword', user_type='freelancer')

@pytest.mark.django_db
def test_create_freelancer_profile_view(client, user):
    # Simular el inicio de sesión del usuario
    client.login(username='testuser', password='testpassword')

    # Datos para crear un perfil de freelancer
    data = {
        'country': 'US',
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Freelance Ave'
    }

    response = client.post(reverse('create_freelancer_profile'), data)
    
    # Verificar que la respuesta es correcta y el perfil se ha creado
    assert response.status_code == 302  # Redirección después de la creación
    assert FreelancerProfile.objects.filter(user=user).exists()

@pytest.mark.django_db
def test_freelancer_profile_detail_view(client, user):
    # Crear un perfil de freelancer para el usuario
    profile = FreelancerProfile.objects.create(
        user=user,
        country='US',
        city='New York',
        phone='1234567890',
        address='1234 Freelance Ave'
    )

    # Simular el inicio de sesión del usuario
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('freelancer_profile_detail', args=[profile.id]))

    # Verificar que la respuesta es correcta y se muestran los detalles
    assert response.status_code == 200
    assert 'New York' in response.content.decode()
    assert '1234 Freelance Ave' in response.content.decode()

@pytest.mark.django_db
def test_freelancer_profile_detail_view(client, user):
    # Crear un perfil de freelancer para el usuario
    profile = FreelancerProfile.objects.create(
        user=user,
        country='US',
        city='New York',
        phone='1234567890',
        address='1234 Freelance Ave'
    )

    # Simular el inicio de sesión del usuario
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('freelancer_profile_detail', args=[profile.id]))

    # Verificar que la respuesta es correcta y se muestran los detalles
    assert response.status_code == 200
    assert 'New York' in response.content.decode()
    assert '1234 Freelance Ave' in response.content.decode()

@pytest.mark.django_db
def test_freelancer_profile_access_without_login(client):
    profile = FreelancerProfile.objects.create(
        user=User.objects.create_user(username='testuser', password='testpassword'),
        country='US',
        city='New York',
        phone='1234567890',
        address='1234 Freelance Ave'
    )

    response = client.get(reverse('freelancer_profile_detail', args=[profile.id]))

    # Verificar que la respuesta es una redirección a la página de login
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_freelancer_profile_creation_invalid_data(client, user):
    # Simular el inicio de sesión del usuario
    client.login(username='testuser', password='testpassword')

    # Datos inválidos para crear un perfil de freelancer
    data = {
        'country': '',  # Campo vacío
        'city': 'New York',
        'phone': '1234567890',
        'address': '1234 Freelance Ave'
    }

    response = client.post(reverse('create_freelancer_profile'), data)

    # Verificar que la respuesta es la página del formulario con errores
    assert response.status_code == 200
    assert 'Este campo no puede estar vacío' in response.content.decode()

def test_work_experience_formset_missing_dates():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': '',  # Fecha de inicio vacía
        'form-0-end_date': '',  # Fecha de fin vacía
        'form-0-company': 'Empresa XYZ',
        'form-0-position': 'Desarrollador',
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'start_date' in formset.forms[0].errors  # Verificar que hay un error en `start_date`
    assert 'end_date' in formset.forms[0].errors  # Verificar que hay un error en `end_date`

def test_work_experience_formset_invalid_position_characters():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': '2024-09-10',
        'form-0-end_date': '2024-09-20',
        'form-0-company': 'Empresa XYZ',
        'form-0-position': 'Desarrollador@#$',  # Caracteres especiales no permitidos
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'position' in formset.forms[0].errors  # Verificar que hay un error en `position`

def test_work_experience_formset_text_instead_of_dates():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': 'diez de septiembre de 2024',  # Formato incorrecto
        'form-0-end_date': 'veinte de septiembre de 2024',  # Formato incorrecto
        'form-0-company': 'Empresa XYZ',
        'form-0-position': 'Desarrollador',
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'start_date' in formset.forms[0].errors  # Verificar que hay un error en `start_date`
    assert 'end_date' in formset.forms[0].errors  # Verificar que hay un error en `end_date`

def test_work_experience_formset_company_name_too_long():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': '2024-09-10',
        'form-0-end_date': '2024-09-20',
        'form-0-company': 'X' * 256,  # Límite de longitud excedido (ej. 255 caracteres)
        'form-0-position': 'Desarrollador',
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'company' in formset.forms[0].errors  # Verificar que hay un error en `company`

def test_work_experience_formset_missing_end_date_for_non_current_job():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': '2024-09-10',
        'form-0-end_date': '',  # Faltante, pero no está marcado como trabajo actual
        'form-0-company': 'Empresa XYZ',
        'form-0-position': 'Desarrollador',
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'end_date' in formset.forms[0].errors  # Verificar que hay un error por falta de `end_date`

def test_work_experience_formset_dates_out_of_range():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': '1900-01-01',  # Fecha fuera del rango permitido
        'form-0-end_date': '1900-12-31',  # Fecha fuera del rango permitido
        'form-0-company': 'Empresa XYZ',
        'form-0-position': 'Desarrollador',
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'start_date' in formset.forms[0].errors  # Verificar que hay un error en `start_date`

def test_work_experience_formset_missing_both_dates_for_current_job():
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-0-start_date': '',  # Fecha faltante
        'form-0-end_date': '',  # Fecha faltante
        'form-0-company': 'Empresa XYZ',
        'form-0-position': 'Desarrollador',
        'form-0-current_job': 'on',  # Marcado como trabajo actual
    }
    formset = WorkExperienceFormSet(data)
    assert not formset.is_valid()
    assert 'start_date' in formset.forms[0].errors  # Verificar que hay un error en `start_date`
