from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField()  # Campo para seleccionar país
    city = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)  # Teléfono
    address = models.CharField(max_length=255, blank=True)  # Dirección
    skills = models.ManyToManyField(Skill, blank=True)

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    country = CountryField()  # Campo para seleccionar país
    city = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)  # Teléfono
    address = models.CharField(max_length=255, blank=True)  # Dirección

# Historial académico
class Education(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="educations")
    institution_name = models.CharField(max_length=255)
    degree_obtained = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.degree_obtained} - {self.institution_name}"

# Experiencia laboral
class WorkExperience(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="work_experiences")
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.position} - {self.company_name}"

# Certificaciones
class Certification(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=255)  # Nombre de la certificación
    issuing_organization = models.CharField(max_length=255)  # Organización emisora
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)  # Puede no tener fecha de expiración
    short_description = models.TextField(max_length=500, blank=True)  # Descripción corta (opcional)

    def __str__(self):
        return f'{self.certification_name} - {self.issuing_organization}'

# Portafolio
class Portfolio(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.url} - {self.freelancer.user.username}'
    