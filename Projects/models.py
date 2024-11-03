from django.db import models
from Users.models import ClientProfile, FreelancerProfile
from django_quill.fields import QuillField
from django.contrib.auth import get_user_model
from .managers import ActiveManager

class Project(models.Model):
    """
    Represents a project in the system.

    Attributes:
        title (str): The title of the project.
        client (ClientProfile): The client associated with the project.
        start_date (date): The date when the project starts.
        due_date (date): The planned due date for the project.
        actual_end_date (date): The actual end date of the project, optional.
        description (str): A detailed description of the project.
        budget (decimal): The budget allocated for the project.
        created_at (datetime): The timestamp when the project was created.
        updated_at (datetime): The timestamp for the last update of the project.
        category (str): The category of the project, defined by CATEGORY_CHOICES.
    """

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

    is_deleted = models.BooleanField(default=False)  # Campo para soft delete

    objects = ActiveManager()  # Administrador que filtra objetos activos
    all_objects = models.Manager()  # Administrador que incluye todos los objetos
    
    title = models.CharField(max_length=255)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="projects")
    start_date = models.DateField()  # Start date of the project
    due_date = models.DateField()     # Planned due date of the project
    actual_end_date = models.DateField(null=True, blank=True)  # Actual end date, optional
    description = QuillField(default="ici")  # Description of the project
    budget = models.DecimalField(max_digits=10, decimal_places=2)  # Budget of the project
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='web_development')

    def days_until_due(self):
        """
        Calculate the number of days until the project is due.

        Returns:
            str: A string indicating the number of days until the due date, or
                 a message if there is no due date.
        """
        if self.due_date:
            delta = (self.due_date - self.start_date).days
            return f"{delta} days to {self.due_date}"
        return "No due date"

    def __str__(self):
        return f"{self.title} by {self.client.user.username}"


class Milestone(models.Model):
    """
    Represents a milestone within a project.

    Attributes:
        project (Project): The project associated with the milestone.
        title (str): The title of the milestone.
        description (str): A detailed description of the milestone.
        due_date (date): The due date for the milestone.
        file (file): An optional file associated with the milestone.
        category (str): The category of the milestone, defined by CATEGORY_CHOICES.
    """

    CATEGORY_CHOICES = [
        ('normal', 'Normal'),
        ('planning', 'Planning'),
        ('development', 'Development'),
        ('review', 'Review'),
        ('delivery', 'Delivery'),
        ('documentation', 'Documentation'),  
    ]
    is_deleted = models.BooleanField(default=False)

    objects = ActiveManager()
    all_objects = models.Manager()
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=255)
    description = QuillField()  # Description of the milestone
    start_date = models.DateField()  # Start date of the milestone
    due_date = models.DateField()  # Due date of the milestone
    file = models.FileField(upload_to='milestone_files/', null=True, blank=True)  # Optional file associated with the milestone
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='development')

    def __str__(self):
        return f"{self.title} - {self.project.title}"


class Task(models.Model):
    """
    Represents a task associated with a milestone.

    Attributes:
        milestone (Milestone): The milestone to which the task belongs.
        title (str): The title of the task.
        description (str): A detailed description of the task.
        due_date (date): The due date for the task.
        priority (str): The priority level of the task, defined by PRIORITY_CHOICES.
        status (str): The current status of the task, defined by STATUS_CHOICES.
        assigned_to (FreelancerProfile): The freelancer assigned to the task.
        attachments (file): Optional attachments for the task.
    """

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
    is_deleted = models.BooleanField(default=False)

    objects = ActiveManager()
    all_objects = models.Manager()
    
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = QuillField()  # Description of the task
    start_date = models.DateField()  # Start date of the task
    due_date = models.DateField()  # Due date of the task
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')  # Priority of the task
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')  # Status of the task
    assigned_to = models.ForeignKey(FreelancerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    attachments = models.FileField(upload_to='task_files/', null=True, blank=True)  # Optional attachments for the task

    def __str__(self):
        return self.title


class ProjectFreelancer(models.Model):
    """
    Represents the association between a project and a freelancer.

    Attributes:
        project (Project): The project associated with the freelancer.
        freelancer (FreelancerProfile): The freelancer associated with the project.
        status (str): The current status of the association, defined by STATUS_CHOICES.
        created_at (datetime): The timestamp when the association was created.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="freelancer_associations")
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="project_associations")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    def __str__(self):
        return f"{self.project.title} - {self.freelancer.user.username} ({self.status})"


User = get_user_model()

class Application(models.Model):
    """
    Represents an application from a freelancer to a project.

    Attributes:
        freelancer (FreelancerProfile): The freelancer who applied.
        project (Project): The project to which the freelancer applied.
        applied_at (datetime): The timestamp when the application was submitted.
    """
    
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='applications')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)  # Timestamp of application submission

    def __str__(self):
        return f"{self.freelancer.user.username} applied to {self.project.title}"


class Contract(models.Model):
    """
    Represents a contract between a freelancer and a project.

    Attributes:
        project (Project): The project associated with the contract.
        freelancer (FreelancerProfile): The freelancer associated with the contract.
        start_date (date): The start date of the contract.
        end_date (date): The end date of the contract, optional.
        status (str): The current status of the contract, defined by STATUS_CHOICES.
    """
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)  # Timestamp of contract start
    end_date = models.DateField(null=True, blank=True)  # Optional end date
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')], default='active')

    def __str__(self):
        return f"Contract for {self.freelancer.user.username} on project {self.project.title}"