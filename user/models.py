from django.db import models
from django.forms import ValidationError
from common.models import CustomUser  # Importing CustomUser from common app
from django.conf import settings

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


from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()  # Get the custom user model

class TaxPayment(models.Model):
    TAX_TYPES = [
        ('Property', 'Property Tax'),
        ('Water', 'Water Tax'),
        ('Professional', 'Professional Tax'),
        ('Other', 'Other'),
    ]

    PAYMENT_METHODS = [
        ('UPI', 'UPI'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Net Banking', 'Net Banking'),
        ('Cash', 'Cash'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Link to CustomUser
    tax_type = models.CharField(max_length=20, choices=TAX_TYPES)
    year = models.IntegerField(null=True, blank=True)  # Only for Property Tax
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")  # Add this line
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tax_type} - ₹{self.amount} - {self.payment_method}"

COMPLAINT_CATEGORIES = [
    ('Road', 'Road Issues'),
    ('Drainage', 'Drainage Problems'),
    ('Water', 'Water Supply Issues'),
    ('Electricity', 'Electricity Complaints'),
    ('Waste', 'Waste Management'),
    ('Other', 'Other'),
]

class Complaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')

    category = models.CharField(max_length=50, choices=COMPLAINT_CATEGORIES)
    ward = models.PositiveIntegerField()
    # name = models.CharField(max_length=100)
    # phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # or use choices if you want

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.category} - Ward {self.ward} by {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # Optional: link to user
    title = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%Y-%m-%d')})"