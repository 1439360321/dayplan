from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.username

