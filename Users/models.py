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

