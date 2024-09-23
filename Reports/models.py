from django.conf import settings
from django.db import models

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the ReportLog instance.

        Returns:
            str: A formatted string showing the user and the type of report generated.
        """
        return f"{self.user} - {self.report_type}"
