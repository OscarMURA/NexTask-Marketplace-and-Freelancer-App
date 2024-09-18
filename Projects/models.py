from django.db import models
from Users.models import ClientProfile

# Definición de la categoría del proyecto primero
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# Ahora define el modelo Project
class Project(models.Model):
    title = models.CharField(max_length=255)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="projects")
    project_duration = models.DateField()
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name="projects")  # Nuevo campo para categoría
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.client.user.username} ({self.category.name})"
