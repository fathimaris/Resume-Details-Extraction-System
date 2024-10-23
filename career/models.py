from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('jobseeker', 'Job Seeker'),
        ('hr', 'HR'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.conf import settings

# models.py

from django.db import models
from django.contrib.auth.models import User

class JobSeeker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)  # Ensure to allow null values
    skills = models.TextField(null=True, blank=True)  # Adjust as necessary
    experience = models.TextField(null=True, blank=True)  # Adjust as necessary
    applied_position = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')  # Adjust the path as necessary

    def __str__(self):
        return self.full_name




class HR(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add any additional fields for HR here
