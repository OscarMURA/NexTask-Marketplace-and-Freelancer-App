from django.conf import settings
from django.db import models

class ReportLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.report_type}"
