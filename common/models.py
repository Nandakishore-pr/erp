from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, role, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not role:
            raise ValueError("Users must have a role")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None):
        user = self.create_user(username, email, phone_number, role='admin', password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('clerk', 'Clerk'),
        ('engineer', 'Engineer'),
        ('user', 'User'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return f"{self.username} ({self.role})"

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    house_number = models.CharField(max_length=50, blank=True, null=True)
    ward_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Engineer Profile Model
class EngineerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='engineer_profile')
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Engineer"

# Clerk Profile Model
class ClerkProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='clerk_profile')
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - Clerk"
