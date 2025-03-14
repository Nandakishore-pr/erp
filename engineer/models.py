from django.db import models
from user.models import UserDocument
from common.models import CustomUser
# Create your models here.
def engineer_document_path(instance, filename):
    return f"engineer_documents/{instance.engineer.id}/{filename}"

class EngineerDocument(models.Model):
    engineer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="engineer_documents")
    user_document = models.ForeignKey(UserDocument, on_delete=models.CASCADE, related_name="engineer_docs")
    clerk = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assigned_clerk", null=True, blank=True)
    description = models.CharField(max_length=250,blank=True,null=True) 
    additional_document = models.FileField(upload_to=engineer_document_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
