# myapp/tests/test_views.py
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
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
    profile = FreelancerProfile.objects.get(user=user)
    assert profile.country == 'US'
    assert profile.city == 'New York'
    assert profile.phone == '1234567890'
    assert profile.address == '1234 Freelance Ave'

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
