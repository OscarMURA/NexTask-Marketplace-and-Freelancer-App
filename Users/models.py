from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser to include user type.
    
    Attributes:
        USER_TYPE_CHOICES (tuple): Defines the types of users ('freelancer' or 'client').
        user_type (str): Specifies the type of user.
    """
    USER_TYPE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    @property
    def is_freelancer(self):
        """
        Returns True if the user is a freelancer, False otherwise.
        """
        return self.user_type == 'freelancer'
    @property
    def is_client(self):
        """
        Returns True if the user is a client, False otherwise.
        """
        return self.user_type == 'client'
class Language(models.Model):
    """
    Represents a spoken language.
    Attributes:
        language (str): Name of the language.
    """
    language = models.CharField(max_length=100, verbose_name=_('Language'))  # Use CharField instead of LanguageField
    def __str__(self):
        return self.language
class Skill(models.Model):
    """
    Represents a skill associated with freelancers.
    Attributes:
        name (str): The name of the skill.
    """
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
class FreelancerProfile(models.Model):
    """
    Represents the profile of a freelancer.
    Attributes:
        user (User): A one-to-one relationship with the User model.
        country (CountryField): Field to select the freelancer's country.
        city (str): City where the freelancer is located.
        phone (str): Phone number of the freelancer.
        address (str): Address of the freelancer.
        skills (ManyToManyField): Skills associated with the freelancer.
        languages (ManyToManyField): Languages spoken by the freelancer.
        avatar (ImageField): Profile picture of the freelancer.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    country = CountryField(blank=False, null=False)  # Campo para seleccionar país
    city = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)  # Teléfono
    address = models.CharField(max_length=255, blank=True)  # Dirección
    skills = models.ManyToManyField(Skill, related_name='freelancers', blank=True)
    languages = models.ManyToManyField('Language', blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='img/defaultFreelancerProfileImage.jpg', blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def __str__(self):
        return self.user.username
    
    def clean(self):
        super().clean()
        if not self.country:
            raise ValueError('El campo "country" es obligatorio.')
        
        
class ClientProfile(models.Model):
    """
    Represents the profile of a client.
    Attributes:
        user (User): A one-to-one relationship with the User model.
        company_name (str): Name of the client's company.
        company_website (str): Website of the client's company.
        country (CountryField): Field to select the client's country.
        city (str): City where the client is located.
        phone (str): Phone number of the client.
        address (str): Address of the client.
        avatar (ImageField): Profile picture of the client.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    country = CountryField(blank=False, null=False)  # Campo para seleccionar país
    city = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)  # Teléfono
    address = models.CharField(max_length=255, blank=True)  # Dirección
    avatar = models.ImageField(upload_to='avatars/', default='img/defaultClientProfileImage.jpg', blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    # Método para calcular el presupuesto total de los proyectos del cliente
    def get_total_budget(self):
        """
        Calculates the total budget of all projects associated with the client.
        Returns:
            float: Total budget of the client's projects.
        """
        return self.projects.aggregate(total_budget=models.Sum('budget'))['total_budget'] or 0
    
    def get_all_projects(self):
        """
        Returns all projects associated with the client.
        Returns:
            QuerySet: All projects associated with this client.
        """
        return self.projects.all()
    
    def clean(self):
        super().clean()
        if not self.country:
            raise ValueError('El campo "country" es obligatorio.')
class Education(models.Model):
    """
    Represents the educational background of a freelancer.
    Attributes:
        freelancer (FreelancerProfile): ForeignKey to the FreelancerProfile model.
        institution_name (str): Name of the educational institution.
        degree_obtained (str): Degree obtained by the freelancer.
        start_date (date): Start date of the education.
        end_date (date): End date of the education.
        description (str): Additional details about the education.
    """
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="educations")
    institution_name = models.CharField(max_length=255, verbose_name=_('Institution Name'))  # Name of the educational institution
    degree_obtained = models.CharField(max_length=255, verbose_name=_('Degree Obtained'))  # Degree obtained by the freelancer
    start_date = models.DateField(verbose_name=_('Start Date'))  # Start date of the education
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))  # End date of the education
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))  # Additional details about the education
    def __str__(self):
        return f"{self.degree_obtained} - {self.institution_name}"
class WorkExperience(models.Model):
    """
    Represents the work experience of a freelancer.
    Attributes:
        freelancer (FreelancerProfile): ForeignKey to the FreelancerProfile model.
        company_name (str): Name of the company where the freelancer worked.
        position (str): Job position held by the freelancer.
        start_date (date): Start date of the work experience.
        end_date (date): End date of the work experience.
        description (str): Additional details about the work experience.
    """
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="work_experiences")
    company_name = models.CharField(max_length=255, verbose_name=_('Company Name'))  # Name of the company
    position = models.CharField(max_length=255, verbose_name=_('Position'))  # Position held by the freelancer
    start_date = models.DateField(verbose_name=_('Start Date'))  # Start date of the work experience
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))  # End date of the work experience
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))  # Additional details about the work experience
    def __str__(self):
        return f"{self.position} - {self.company_name}"
    
    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("La fecha de finalización debe ser posterior a la fecha de inicio.")
class Certification(models.Model):
    """
    Represents certifications obtained by a freelancer.
    Attributes:
        freelancer (FreelancerProfile): ForeignKey to the FreelancerProfile model.
        certification_name (str): Name of the certification.
        issuing_organization (str): Organization that issued the certification.
        issue_date (date): Date when the certification was issued.
        expiration_date (date): Expiration date of the certification (if applicable).
        short_description (str): Short description of the certification.
    """
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=255, verbose_name=_('Certification Name'))  # Name of the certification
    issuing_organization = models.CharField(max_length=255, verbose_name=_('Issuing Organization'))  # Organization that issued the certification
    issue_date = models.DateField(verbose_name=_('Issue Date'))  # Date when the certification was issued
    expiration_date = models.DateField(blank=True, null=True, verbose_name=_('Expiration Date'))  # Expiration date of the certification
    short_description = models.TextField(max_length=500, blank=True, verbose_name=_('Short Description'))  # Short description of the certification
    def __str__(self):
        return f'{self.certification_name} - {self.issuing_organization}'
class Portfolio(models.Model):
    """
    Represents the portfolio of a freelancer.
    Attributes:
        freelancer (FreelancerProfile): ForeignKey to the FreelancerProfile model.
        url (str): URL of the portfolio.
        description (str): Description of the portfolio.
    """
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    url = models.URLField(blank=True, verbose_name=_('Portfolio URL'))  # URL of the portfolio
    description = models.TextField(blank=True, verbose_name=_('Description'))  # Description of the portfolio
    def __str__(self):
        return f'{self.url} - {self.freelancer.user.username}'