

# Create your models here.
from django.db import models
from datetime import date
from common.models import ClerkProfile
from engineer.models import EngineerDocument
from common.models import CustomUser
from django.conf import settings


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

class AdminToClerkSuggestion(models.Model):
    document = models.ForeignKey(ClerkDocument, on_delete=models.CASCADE, related_name="admin_suggestions")
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_clerk_suggestions")
    clerk = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_admin_suggestions")
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion from {self.admin} to {self.clerk}"
    
class LeaveRequest(models.Model):
    clerk = models.ForeignKey(ClerkProfile, on_delete=models.CASCADE)  # Make sure this is correct
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending")



class VideoCall(models.Model):
    clerk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clerk_calls")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_calls")
    scheduled_time = models.DateTimeField()
    meeting_link = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.meeting_link:
            self.meeting_link = f"https://meet.jit.si/{self.clerk.username}_{self.user.username}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.clerk} - {self.user} at {self.scheduled_time}"