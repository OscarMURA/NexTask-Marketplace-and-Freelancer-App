from django.db import models
from Users.models import ClientProfile
from django_quill.fields import QuillField


class Project(models.Model):
    
    CATEGORY_CHOICES = [
        ('web_development', 'Web Development'),
        ('mobile_app_development', 'Mobile App Development'),
        ('graphic_design', 'Graphic Design'),
        ('content_writing', 'Content Writing'),
        ('digital_marketing', 'Digital Marketing'),
        ('seo', 'SEO'),
        ('video_editing', 'Video Editing'),
        ('data_entry', 'Data Entry'),
        ('translation', 'Translation Services'),
        ('customer_support', 'Customer Support'),
        ('software_development', 'Software Development'),
        ('it_networking', 'IT & Networking'),
        ('ecommerce', 'E-commerce Development'),
        ('virtual_assistance', 'Virtual Assistance'),
        ('project_management', 'Project Management'),
        ('accounting_finance', 'Accounting & Finance'),
        ('legal_consulting', 'Legal Consulting'),
    ]

    title = models.CharField(max_length=255)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="projects")
    start_date = models.DateField()  # Fecha de inicio del proyecto
    due_date = models.DateField()    # Fecha de vencimiento planeada
    actual_end_date = models.DateField(null=True, blank=True)  # Fecha real de finalización del proyecto, opcional
    description = QuillField(default="ici")  # Descripción del proyecto
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='web_development')

    
    def days_until_due(self):
        if self.due_date:
            delta = (self.due_date - self.start_date).days
            return f"{delta}  days to {self.due_date}"
        return "Sin fecha final"

    def __str__(self):
        return f"{self.title} by {self.client.user.username})"


class Milestone(models.Model):
    CATEGORY_CHOICES = [
        ('normal', 'Normal'),
        ('planning', 'Planning'),
        ('development', 'Development'),
        ('review', 'Review'),
        ('delivery', 'Delivery'),
        ('documentation', 'Documentation'),  
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=255)
    description = QuillField()
    due_date = models.DateField()
    file = models.FileField(upload_to='milestone_files/', null=True, blank=True)  # Archivo relacionado con el hito, opcional
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='development')


    def __str__(self):
        return f"{self.title} - {self.project.title}"