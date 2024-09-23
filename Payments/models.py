from django.db import models
from Projects.models import Project
from Users.models import ClientProfile, FreelancerProfile

class Payment(models.Model):
    """
    Payment model to handle payments associated with projects.

    Attributes:
        project (ForeignKey): Reference to the Project associated with the payment.
        client (ForeignKey): Reference to the ClientProfile making the payment.
        freelancer (ForeignKey): Reference to the FreelancerProfile receiving the payment.
        amount (DecimalField): The amount of the payment in decimal format.
        status (CharField): The status of the payment, with choices for 'pending', 'completed', or 'failed'.
        created_at (DateTimeField): Timestamp for when the payment record was created.
    """

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
        """
        String representation of the Payment instance.

        Returns:
            str: A string indicating the payment details including the project title and amount.
        """
        return f"Payment for {self.project.title} - {self.amount} USD"
