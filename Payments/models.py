from django.db import models
from django.db import models
from Projects.models import Project
from Users.models import ClientProfile, FreelancerProfile

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.project.title} - {self.amount} USD"
