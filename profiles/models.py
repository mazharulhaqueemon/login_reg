from django.db import models

from accounts.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    division = models.CharField(max_length=100, blank=True, null=True)
    upozila = models.CharField(max_length=100, blank=True, null=True)