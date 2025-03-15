

# Create your models here.
from django.db import models
from datetime import date
from common.models import ClerkProfile
from engineer.models import EngineerDocument
from common.models import CustomUser

class Attendance(models.Model):
    clerk = models.ForeignKey(ClerkProfile, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(default=date.today)
    time = models.TimeField(auto_now_add=True)
    session = models.CharField(max_length=20, choices=[("Morning", "Morning"), ("Afternoon", "Afternoon")])
    status = models.CharField(max_length=10, default="Present")

    def __str__(self):
        return f"{self.employee_name} - {self.date} - {self.session}"
    
def clerk_document_path(instance, filename):
    return f"clerk_documents/{instance.clerk.id}/{filename}"

class ClerkDocument(models.Model):
    clerk = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="clerk_documents")
    engineer_document = models.ForeignKey(EngineerDocument, on_delete=models.CASCADE, related_name="clerk_docs")
    additional_document = models.FileField(upload_to=clerk_document_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250,blank=True,null=True) 
    status = models.BooleanField(default=False)
    
class LeaveRequest(models.Model):
    clerk = models.ForeignKey(ClerkProfile, on_delete=models.CASCADE)  # Make sure this is correct
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending")

