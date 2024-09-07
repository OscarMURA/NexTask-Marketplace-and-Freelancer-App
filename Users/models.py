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

# models.py
class Education(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    entity_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

class Certification(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    entity_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    certification_id = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

class Portfolio(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
