from django.db import models
from common.models import CustomUser  # Importing CustomUser from common app

def user_document_path(instance, filename):
    """Generate file path for a user's document upload"""
    return f"user_documents/{instance.user.id}/{filename}"


class UserDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents")
    engineer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assigned_documents", null=True, blank=True)  # Engineer assigned
    document = models.FileField(upload_to=user_document_path)  # No restriction on file type
    description = models.CharField(max_length=250,blank=True,null=True) 
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.document.name} - {'Approved' if self.status else 'Pending'}"
