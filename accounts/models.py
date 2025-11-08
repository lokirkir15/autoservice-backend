from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    is_customer = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)

    def __str__(self):
        return self.get_username()
