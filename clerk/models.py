

# Create your models here.
from django.db import models
from datetime import date
from common.models import ClerkProfile

class Attendance(models.Model):
    clerk = models.ForeignKey(ClerkProfile, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(default=date.today)
    time = models.TimeField(auto_now_add=True)
    session = models.CharField(max_length=20, choices=[("Morning", "Morning"), ("Afternoon", "Afternoon")])
    status = models.CharField(max_length=10, default="Present")

    def __str__(self):
        return f"{self.employee_name} - {self.date} - {self.session}"

    