from django.db import models
from django.contrib.auth.models import AbstractUser

# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractUser):
    phone = models.TextField(unique=True, max_length=30)

    class Meta:
        ordering = ["id"]
