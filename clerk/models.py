

# Create your models here.
from django.db import models
from datetime import date

class Attendance(models.Model):
    employee_name = models.CharField(max_length=100)
    date = models.DateField(default=date.today)
    time = models.TimeField(auto_now_add=True)
    session = models.CharField(max_length=20, choices=[("Morning", "Morning"), ("Afternoon", "Afternoon")])
    status = models.CharField(max_length=10, default="Present")

    def __str__(self):
        return f"{self.employee_name} - {self.date} - {self.session}"
