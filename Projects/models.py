from django.db import models
from Users.models import ClientProfile, FreelancerProfile
from django_quill.fields import QuillField
from django.contrib.auth import get_user_model

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
    

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = QuillField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(FreelancerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    attachments = models.FileField(upload_to='task_files/', null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    

class ProjectFreelancer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="freelancer_associations")
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="project_associations")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.freelancer.user.username} ({self.status})"    



User = get_user_model()


class Application(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='applications')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.user.username} applied to {self.project.title}"
    
    
class Contract(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')], default='active')

    def __str__(self):
        return f"Contract for {self.freelancer.user.username} on project {self.project.title}"




