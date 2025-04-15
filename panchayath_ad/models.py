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

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
    
class Notice(models.Model):
    RECIPIENT_CHOICES = [
        ('public', 'Public'),
        ('clerks', 'Clerks'),
        ('engineers', 'Engineers'),
        ('everyone', 'Everyone'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='notices/', blank=True, null=True)
    recipient = models.CharField(max_length=20, choices=RECIPIENT_CHOICES)
    date = models.DateField()

    def __str__(self):
        return self.title

