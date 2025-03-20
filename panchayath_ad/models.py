from django.db import models
from common.models import CustomUser
from clerk.models import ClerkDocument

# Create your models here.

def admin_document_path(instance, filename):
    return f"admin_documents/{instance.admin.id}/{filename}"

class AdminDocument(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin_documents")
    clerk_document = models.ForeignKey(ClerkDocument, on_delete=models.CASCADE, related_name="admin_docs")
    final_document = models.FileField(upload_to=admin_document_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250,blank=True,null=True) 
    status = models.BooleanField(default=False)

