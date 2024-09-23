# myapp/tests/test_models.py
import pytest
from django_countries.fields import Country
from Users.models import User, FreelancerProfile, Skill, Education, WorkExperience, Certification, Portfolio, ClientProfile
from django.core.exceptions import ValidationError

@pytest.fixture
def user():
    return User.objects.create_user(
        username="john_doe",
        password="password123",
        user_type="freelancer"
    )

@pytest.fixture
def freelancer_profile(user):
    return FreelancerProfile.objects.create(
        user=user,
        country="US",
        city="New York",
        phone="123456789",
        address="1234 Freelance Ave"
    )

@pytest.mark.django_db
def test_freelancer_profile_creation(freelancer_profile):
    freelancer = FreelancerProfile.objects.get(id=freelancer_profile.id)
    assert freelancer.user.username == "john_doe"
    assert freelancer.city == "New York"
    assert freelancer.phone == "123456789"
    assert freelancer.address == "1234 Freelance Ave"
    assert freelancer.country == Country(code="US")

@pytest.mark.django_db
def test_freelancer_skills(freelancer_profile):
    skill = Skill.objects.create(name="Python")
    freelancer_profile.skills.add(skill)
    assert skill in freelancer_profile.skills.all()

@pytest.mark.django_db
def test_freelancer_education(freelancer_profile):
    education = Education.objects.create(
        freelancer=freelancer_profile,
        institution_name="MIT",
        degree_obtained="Bachelor of Computer Science",
        start_date="2015-09-01",
        end_date="2019-06-30",
        description="Computer Science program"
    )
    assert education.institution_name == "MIT"
    assert education.degree_obtained == "Bachelor of Computer Science"
    assert education.freelancer == freelancer_profile

@pytest.mark.django_db
def test_freelancer_work_experience(freelancer_profile):
    work_experience = WorkExperience.objects.create(
        freelancer=freelancer_profile,
        company_name="Tech Corp",
        position="Software Engineer",
        start_date="2020-01-01",
        end_date="2022-12-31",
        description="Worked on backend development"
    )
    assert work_experience.company_name == "Tech Corp"
    assert work_experience.position == "Software Engineer"
    assert work_experience.freelancer == freelancer_profile

@pytest.mark.django_db
def test_freelancer_certifications(freelancer_profile):
    certification = Certification.objects.create(
        freelancer=freelancer_profile,
        certification_name="AWS Certified Solutions Architect",
        issuing_organization="Amazon",
        issue_date="2021-05-01",
        expiration_date=None,
        short_description="AWS Solutions Architect certification"
    )
    assert certification.certification_name == "AWS Certified Solutions Architect"
    assert certification.issuing_organization == "Amazon"
    assert certification.freelancer == freelancer_profile

@pytest.mark.django_db
def test_freelancer_portfolio(freelancer_profile):
    portfolio = Portfolio.objects.create(
        freelancer=freelancer_profile,
        url="http://portfolio.example.com",
        description="My personal portfolio"
    )
    assert portfolio.url == "http://portfolio.example.com"
    assert portfolio.freelancer == freelancer_profile

@pytest.mark.django_db
def test_client_profile_creation():
    user = User.objects.create_user(
        username="client_user",
        password="password123",
        user_type="client"
    )

    client_profile = ClientProfile.objects.create(
        user=user,
        company_name="Tech Co.",
        company_website="http://techco.com",
        country="US",
        city="San Francisco",
        phone="123456789",
        address="1234 Tech St."
    )

    assert client_profile.user.username == "client_user"
    assert client_profile.company_name == "Tech Co."
    assert client_profile.country == Country(code="US")
    assert client_profile.city == "San Francisco"

@pytest.mark.django_db
def test_unique_skill_creation():
    skill = Skill.objects.create(name="Django")

    assert skill.name == "Django"

    # Prueba que no se permita duplicar el nombre de la habilidad
    with pytest.raises(Exception):
        Skill.objects.create(name="Django")

@pytest.mark.django_db
def test_freelancer_skill_assignment():
    user = User.objects.create_user(
        username="freelancer_user",
        password="password123",
        user_type="freelancer"
    )
    freelancer_profile = FreelancerProfile.objects.create(
        user=user,
        country="US",
        city="New York",
        phone="123456789",
        address="1234 Freelance Ave"
    )

    skill_python = Skill.objects.create(name="Python")
    skill_django = Skill.objects.create(name="Django")

    freelancer_profile.skills.add(skill_python)
    freelancer_profile.skills.add(skill_django)

    assert skill_python in freelancer_profile.skills.all()
    assert skill_django in freelancer_profile.skills.all()

@pytest.mark.django_db
def test_freelancer_profile_optional_fields():
    user = User.objects.create_user(username='testfreelancer', password='testpassword')

    # Crear perfil sin campos opcionales
    freelancer_profile = FreelancerProfile(
        user=user,
        country="US"
    )
    try:
        freelancer_profile.full_clean()
        freelancer_profile.save()
    except ValidationError:
        pytest.fail("No debería fallar si los campos opcionales están vacíos")

    # Verificar que los campos opcionales estén vacíos
    assert freelancer_profile.city == ""
    assert freelancer_profile.phone == ""
    assert freelancer_profile.address == ""
    assert freelancer_profile.skills.count() == 0

@pytest.mark.django_db
def test_client_profile_optional_fields():
    user = User.objects.create_user(username='testclient', password='testpassword')

    # Crear perfil sin campos opcionales
    client_profile = ClientProfile(
        user=user,
        company_name="Test Company",
        country="US"
    )
    try:
        client_profile.full_clean()
        client_profile.save()
    except ValidationError:
        pytest.fail("No debería fallar si los campos opcionales están vacíos")

    # Verificar que los campos opcionales estén vacíos
    assert client_profile.company_website == ""
    assert client_profile.city == ""
    assert client_profile.phone == ""
    assert client_profile.address == ""

@pytest.mark.django_db
def test_freelancer_profile_skills():
    # Crear un usuario de prueba
    user = User.objects.create_user(username='testfreelancer', password='testpassword')

    # Crear varias habilidades
    skill1 = Skill.objects.create(name="Python")
    skill2 = Skill.objects.create(name="Django")
    skill3 = Skill.objects.create(name="JavaScript")

    # Crear perfil de freelancer y asociar habilidades
    freelancer_profile = FreelancerProfile(
        user=user,
        country="US",
        city="Test City",
        phone="1234567890",
        address="Test Address"
    )
    freelancer_profile.save()
    freelancer_profile.skills.set([skill1, skill2, skill3])
    freelancer_profile.save()

    # Verificar que las habilidades se han asociado correctamente
    assert freelancer_profile.skills.count() == 3
    assert skill1 in freelancer_profile.skills.all()
    assert skill2 in freelancer_profile.skills.all()
    assert skill3 in freelancer_profile.skills.all()

@pytest.mark.django_db
def test_freelancer_profile_missing_required_fields(user):
    # Intenta crear un perfil sin el campo obligatorio 'country'
    freelancer_profile = FreelancerProfile(
        user=user,
        city="New York",
        phone="123456789",
        address="1234 Freelance Ave"
    )
    
    # Llama a full_clean() para forzar la validación y verificar que se lanza un ValueError
    with pytest.raises(ValueError) as exc_info:
        freelancer_profile.full_clean()  # Esto lanzará el ValueError por 'country' faltante

    # Verifica que el mensaje del error sea el esperado
    assert str(exc_info.value) == 'El campo "country" es obligatorio.'


@pytest.mark.django_db
def test_freelancer_profile_phone_length(freelancer_profile):
    freelancer_profile.phone = "1" * 21
    with pytest.raises(ValidationError):
        freelancer_profile.full_clean()

@pytest.mark.django_db
def test_freelancer_profile_cascade_delete(freelancer_profile):
    work_experience = WorkExperience.objects.create(
        freelancer=freelancer_profile,
        company_name="Tech Corp",
        position="Software Engineer",
        start_date="2020-01-01",
        end_date="2022-12-31"
    )
    freelancer_profile.delete()
    assert WorkExperience.objects.filter(id=work_experience.id).count() == 0



@pytest.mark.django_db
def test_freelancer_profile_update(freelancer_profile):
    freelancer_profile.city = "Los Angeles"
    freelancer_profile.save()

    updated_profile = FreelancerProfile.objects.get(id=freelancer_profile.id)
    assert updated_profile.city == "Los Angeles"
