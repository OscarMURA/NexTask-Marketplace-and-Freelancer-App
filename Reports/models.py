from django.conf import settings
from django.db import models
from Projects.models import Project
from django.contrib.auth import get_user_model


User = get_user_model()


class ReportLog(models.Model):
    """
    Model to log report generation details.

    Attributes:
        user (ForeignKey): A reference to the user who generated the report. 
                           This field is linked to the User model defined in settings.
        report_type (CharField): A string that describes the type of report generated (e.g., 'monthly', 'weekly').
        generated_at (DateTimeField): The timestamp of when the report was generated, 
                                       automatically set to the current time when the object is created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    data = models.JSONField(default=dict)  # O el tipo de campo que hayas definido para `data`
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.project.title} - {self.report_type}"