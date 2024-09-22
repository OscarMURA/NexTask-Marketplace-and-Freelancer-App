from django.db import models
from django.contrib.auth.models import User

class ReportLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.report_type}"
