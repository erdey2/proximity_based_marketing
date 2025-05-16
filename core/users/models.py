from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 'Admin'
    MARKETER = 'Marketer'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MARKETER, 'Marketer'),
    ]

    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MARKETER)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f'user {self.username} - {self.email}'

class UserPreferences(models.Model):
    """Stores user ad preferences"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    preferred_categories = models.JSONField(default=list)  # Example: ["soup", "food"]
    ad_frequency = models.IntegerField(default=5)  # Max ads per day

    def __str__(self):
        return f"Preferences for {self.user.username}"

