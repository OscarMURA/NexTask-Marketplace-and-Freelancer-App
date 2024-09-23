import pytest
from django.urls import reverse
from Users.models import *

@pytest.mark.django_db
def test_freelancer_signup_view_get(client):
    """Verifica que la vista de registro de freelancer responda correctamente"""
    response = client.get(reverse('register_freelancer'))
    assert response.status_code == 200
    assert 'Users/freelancer_signup.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_freelancer_signup_view_post(client):
    """Verifica que un freelancer se registre correctamente"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'testfreelancer',
        'email': 'freelancer@test.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'country': 'CO',
        'city': 'TestCity',
        'phone': '123456789',
        'address': 'Test Address',
    })
    
    # Verifica redirección después del POST exitoso
    assert response.status_code == 302
    
    # Verifica que el usuario y el perfil de freelancer fueron creados
    assert User.objects.filter(username='testfreelancer').exists()
    assert FreelancerProfile.objects.filter(user__username='testfreelancer').exists()
    
    # Verifica los datos del perfil
    freelancer_profile = FreelancerProfile.objects.get(user__username='testfreelancer')
    assert freelancer_profile.city == 'TestCity'

@pytest.mark.django_db
def test_freelancer_signup_password_mismatch(client):
    """Verifica que el formulario falle cuando las contraseñas no coinciden"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'testfreelancer2',
        'email': 'freelancer2@test.com',
        'password1': 'password123',
        'password2': 'differentpassword123',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'country': 'CO',
        'city': 'TestCity',
        'phone': '123456789',
        'address': 'Test Address',
    })
    
    # Imprime el contenido de la respuesta para ver el error
    print(response.content.decode())
    
    # Verifica que la respuesta no sea de redirección y se mantenga en la página
    assert response.status_code == 200
    assert "password" in response.content.decode().lower()


@pytest.mark.django_db
def test_freelancer_signup_duplicate_username(client):
    """Verifica que no se permita el registro con un nombre de usuario duplicado"""
    # Primero se crea un usuario
    User.objects.create_user(username='testfreelancer', password='password123')
    
    # Intentamos registrar otro usuario con el mismo nombre de usuario
    response = client.post(reverse('register_freelancer'), data={
        'username': 'testfreelancer',  # Mismo nombre de usuario
        'email': 'freelancer@test.com',
        'password1': 'password123@',
        'password2': 'password123@',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'country': 'CO',
        'city': 'TestCity',
        'phone': '123456789',
        'address': 'Test Address',
    })
    
    # Verifica que la respuesta sea 200 con un mensaje de error
    assert response.status_code == 200
    assert "A user with that username already exists." in response.content.decode()

@pytest.mark.django_db
def test_freelancer_signup_missing_required_field(client):
    """Verifica que el formulario falle si falta un campo obligatorio"""
    response = client.post(reverse('register_freelancer'), data={
        'username': '',  # Faltando el nombre de usuario
        'email': 'freelancer@test.com',
        'password1': 'password123',
        'password2': 'password123',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'country': 'CO',
        'city': 'TestCity',
        'phone': '123456789',
        'address': 'Test Address',
    })
    
    # Verifica que la respuesta sea 200 y que se muestre un mensaje de error
    assert response.status_code == 200
    assert "This field is required." in response.content.decode()

@pytest.mark.django_db
def test_freelancer_signup_invalid_email(client):
    """Verifica que el formulario falle con un correo electrónico inválido"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'testfreelancer3',
        'email': 'invalid-email',  # Correo no válido
        'password1': 'password123',
        'password2': 'password123',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'country': 'CO',
        'city': 'TestCity',
        'phone': '123456789',
        'address': 'Test Address',
    })
    
    # Verifica que la respuesta sea 200 y que se muestre un mensaje de error
    assert response.status_code == 200
    assert "Enter a valid email address." in response.content.decode()

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from Users.models import FreelancerProfile

@pytest.mark.django_db
def test_freelancer_signup_form_display(client):
    """Verifica que el formulario de registro de freelancer se muestre correctamente"""
    response = client.get(reverse('register_freelancer'))
    assert response.status_code == 200
    assert 'Users/freelancer_signup.html' in [t.name for t in response.templates]
    assert 'form' in response.context

@pytest.mark.django_db
def test_freelancer_signup_form_invalid_data(client):
    """Verifica que el formulario de registro de freelancer maneje datos inválidos correctamente"""
    response = client.post(reverse('register_freelancer'), data={
        'username': '',
        'email': 'invalid-email',
        'password1': 'password123',
        'password2': 'differentpassword',
        'first_name': '',
        'last_name': '',
        'country': '',
        'city': '',
        'phone': '',
        'address': '',
    })
    
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert "The two password fields didn't match." in response.content.decode()
    assert "This field is required." in response.content.decode()

@pytest.mark.django_db
def test_freelancer_signup_form_invalid_data(client):
    """Verifica que el formulario de registro de freelancer maneje datos inválidos correctamente"""
    response = client.post(reverse('register_freelancer'), data={
        'username': '',
        'email': 'invalid-email',
        'password1': 'password123',
        'password2': 'differentpassword',
        'first_name': '',
        'last_name': '',
        'country': '',
        'city': '',
        'phone': '',
        'address': '',
    })
    
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert 'username' in response.context['form'].errors
    assert 'email' in response.context['form'].errors
    assert 'password2' in response.context['form'].errors

@pytest.mark.django_db
def test_login_redirect_to_welcome(client):
    """Verifica que un usuario que inicia sesión correctamente sea redirigido a la página de bienvenida"""
    
    # Registra un nuevo freelancer
    client.post(reverse('register_freelancer'), data={
        'username': 'testlogin',
        'email': 'login@test.com',
        'password1': 'password123',
        'password2': 'password123',
        'first_name': 'Test',
        'last_name': 'Login',
        'country': 'CO',
        'city': 'TestCity',
        'phone': '123456789',
        'address': 'Test Address',
    })
    
    # Inicia sesión con las credenciales del freelancer
    response = client.post(reverse('login'), data={
        'username': 'testlogin',
        'password': 'password123'
    }, follow=True)
    
    # Verifica que la redirección a la página de bienvenida es exitosa
    assert response.status_code == 200
    assert "Bienvenido" in response.content.decode() or "Welcome" in response.content.decode()

@pytest.mark.django_db
def test_freelancer_signup_successful_with_extra_fields(client):
    """Verifica que un freelancer se registre correctamente con campos adicionales"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'extra_fields_freelancer',
        'email': 'extra@test.com',
        'password1': 'password123!',
        'password2': 'password123!',
        'first_name': 'Extra',
        'last_name': 'Fields',
        'country': 'CO',
        'city': 'ExtraCity',
        'phone': '987654321',
        'address': 'Extra Address',
    })
    
    assert response.status_code == 302  # Redirección después del registro
    assert User.objects.filter(username='extra_fields_freelancer').exists()
    assert FreelancerProfile.objects.filter(user__username='extra_fields_freelancer').exists()

@pytest.mark.django_db
def test_freelancer_signup_form_required_fields(client):
    """Verifica que se muestren errores si faltan campos requeridos"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'required_fields_test',
        'email': '',  # Faltando el email
        'password1': '',
        'password2': '',
        'first_name': 'Test',
        'last_name': 'Required',
        'country': 'CO',
        'city': 'RequiredCity',
        'phone': '123456789',
        'address': 'Required Address',
    })
    
    assert response.status_code == 200
    assert "This field is required." in response.content.decode()

@pytest.mark.django_db
def test_freelancer_signup_success_with_valid_email(client):
    """Verifica que un freelancer se registre correctamente con un email válido"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'valid_email_freelancer',
        'email': 'validemail@test.com',
        'password1': 'password123!',
        'password2': 'password123!',
        'first_name': 'Valid',
        'last_name': 'Email',
        'country': 'CO',
        'city': 'ValidCity',
        'phone': '123456789',
        'address': 'Valid Address',
    })
    
    assert response.status_code == 302
    assert User.objects.filter(username='valid_email_freelancer').exists()

@pytest.mark.django_db
def test_portfolio_register_view_get(client):
    """Verifica que la vista de registro de portafolio se muestre correctamente"""
    
    # Crea un freelancer y lo autentica
    user = User.objects.create_user(username='freelancer_portfolio', password='password123')
    FreelancerProfile.objects.create(user=user)
    
    client.login(username='freelancer_portfolio', password='password123')
    
    # Realiza una petición GET a la vista de registro de portafolio
    response = client.get(reverse('portfolio_register'))
    
    # Verifica que el formulario de portafolio y el template se están renderizando
    assert response.status_code == 200
    assert 'portfolio_formset' in response.context
    assert 'Users/portfolio_register.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_freelancer_signup_missing_fields(client):
    """Verifica que se muestren errores si faltan campos obligatorios"""
    
    # Intenta registrar un freelancer con datos faltantes
    response = client.post(reverse('register_freelancer'), data={
        'username': '',  # Faltando el nombre de usuario
        'email': 'freelancer@test.com',
        'password1': 'password123',
        'password2': 'password123',
    })
    
    # Verifica que el formulario devuelva un error
    assert response.status_code == 200
    assert "This field is required." in response.content.decode()

@pytest.mark.django_db
def test_welcome_view(client):
    """Verifica que la página de bienvenida se muestre correctamente"""
    
    # Crea un freelancer y lo autentica
    user = User.objects.create_user(username='freelancer_welcome', password='password123')
    FreelancerProfile.objects.create(user=user)
    
    client.login(username='freelancer_welcome', password='password123')
    
    # Realiza una petición GET a la vista de bienvenida
    response = client.get(reverse('welcome'))
    
    # Verifica que el template correcto se está renderizando
    assert response.status_code == 200
    assert 'Users/welcome.html' in [t.name for t in response.templates]
    assert "Welcome" in response.content.decode()
    assert "You have successfully completed your registration!" in response.content.decode()

@pytest.mark.django_db
def test_freelancer_signup_username_max_length(client):
    """Verifica que no se pueda registrar un freelancer con un username demasiado largo"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'a' * 151,  # Excede el máximo de 150 caracteres de Django
        'email': 'freelancer@test.com',
        'password1': 'password123',
        'password2': 'password123',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'country': 'CO',
        'city': 'TestCity',
        'phone': '123456789',
        'address': 'Test Address',
    })
    
    assert response.status_code == 200
    assert "Ensure this value has at most 150 characters" in response.content.decode()

@pytest.mark.django_db
def test_freelancer_signup_optional_fields(client):
    """Verifica que el registro de freelancer funcione sin los campos opcionales"""
    response = client.post(reverse('register_freelancer'), data={
        'username': 'testoptional',
        'email': 'optional@test.com',
        'password1': 'StrongPassword123!',
        'password2': 'StrongPassword123!',
        'first_name': 'Test',
        'last_name': 'Freelancer',
        'country': 'CO',
        'city': 'TestCity',
        # No se incluyen 'phone' ni 'address'
    })
    
    # Verifica que el registro haya sido exitoso
    assert response.status_code == 302  # Código de redirección
    assert User.objects.filter(username='testoptional').exists()  # Verifica que el usuario se haya creado
    freelancer_profile = FreelancerProfile.objects.get(user__username='testoptional')
    assert freelancer_profile.phone == ''  # Valor por defecto para phone
    assert freelancer_profile.address == ''


#@pytest.mark.django_db
#def test_freelancer_signup_invalid_phone(client):
#    """Verifica que el registro de freelancer falle con un número de teléfono no válido"""
#    response = client.post(reverse('register_freelancer'), data={
#        'username': 'invalidphone',
#        'email': 'phone@test.com',
#        'password1': 'password123',
#        'password2': 'password123',
#        'first_name': 'Test',
#        'last_name': 'Freelancer',
#        'country': 'CO',
#        'city': 'TestCity',
#        'phone': 'invalid_phone',  # Número no válido
#        'address': 'Test Address',
#    })
    
#    assert response.status_code == 200
#    assert "Enter a valid phone number" in response.content.decode()

@pytest.mark.django_db
def test_login_redirect_by_user_type(client):
    """Verifica que se redirija correctamente a los freelancers o clientes después de iniciar sesión"""
    
    # Crear y loguear un freelancer
    freelancer = User.objects.create_user(username='freelancer', password='password123', user_type='freelancer')
    FreelancerProfile.objects.create(user=freelancer)
    
    response = client.post(reverse('login'), data={
        'username': 'freelancer',
        'password': 'password123'
    })
    assert response.status_code == 302
    assert response.url == reverse('home_freelancer')
    
    # Crear y loguear un cliente
    client_user = User.objects.create_user(username='clientuser', password='password123', user_type='client')
    ClientProfile.objects.create(user=client_user, company_name='Test Company')
    
    response = client.post(reverse('login'), data={
        'username': 'clientuser',
        'password': 'password123'
    })
    assert response.status_code == 302
    assert response.url == reverse('home_client')

@pytest.mark.django_db
def test_logout_and_protected_view_access(client):
    """Verifica que un usuario no logueado no pueda acceder a vistas protegidas"""
    
    # Crear y loguear un freelancer
    user = User.objects.create_user(username='freelancer', password='StrongPassword123!', user_type='freelancer')
    FreelancerProfile.objects.create(user=user)
    
    client.login(username='freelancer', password='StrongPassword123!')
    
    # Verifica acceso a vista protegida
    response = client.get(reverse('home_freelancer'))
    assert response.status_code == 200
    
    # Cerrar sesión
    client.logout()
    
    # Intentar acceder a una vista protegida después del logout
    response = client.get(reverse('home_freelancer'))
    assert response.status_code == 302  # Espera redirección a la página de login
    assert response.url == reverse('login') + '?next=' + reverse('home_freelancer')

@pytest.mark.django_db
def test_freelancer_profile_update(client):
    """Verifica que un freelancer pueda actualizar su perfil correctamente"""
    
    # Crear y loguear un freelancer
    user = User.objects.create_user(username='freelancer_update', password='password123', user_type='freelancer')
    freelancer_profile = FreelancerProfile.objects.create(user=user, city="OldCity")
    
    client.login(username='freelancer_update', password='password123')
    
    # Actualizar perfil
    response = client.post(reverse('profile_settings'), data={
        'username': 'freelancer_update',
        'email': 'update@test.com',
        'first_name': 'Updated',
        'last_name': 'Freelancer',
        'city': 'NewCity',  # Nuevo valor para la ciudad
        'country': 'CO',
        'phone': '987654321',
        'address': 'Updated Address',
    })
    
    # Verifica que la actualización fue exitosa
    assert response.status_code == 200
    freelancer_profile.refresh_from_db()
    assert freelancer_profile.city == 'NewCity'
    assert freelancer_profile.phone == '987654321'
