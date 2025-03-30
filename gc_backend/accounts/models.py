from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    company_id = models.CharField(max_length=100, unique=True)  # Company ID field
    role = models.CharField(max_length=50, choices=[  # Role field with predefined choices
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ], default='employee')

    # Add missing fields
    post = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.role} (Company: {self.company_id})"