from django.db import models
from Users.models import ClientProfile
from django_quill.fields import QuillField


class Project(models.Model):
    title = models.CharField(max_length=255)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="projects")
    start_date = models.DateField()  # Fecha de inicio del proyecto
    due_date = models.DateField()    # Fecha de vencimiento planeada
    actual_end_date = models.DateField(null=True, blank=True)  # Fecha real de finalización del proyecto, opcional
    description = QuillField(default="ici")  # Descripción del proyecto
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.client.user.username})"

