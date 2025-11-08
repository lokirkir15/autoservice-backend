from django.db import models
from django.conf import settings

class Workstation(models.Model):
    name = models.CharField("Nazwa stanowiska", max_length=50)
    is_active = models.BooleanField("Aktywne", default=True)

    def __str__(self):
        return self.name

class TechnicianProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='technician_profile'
    )
    # tu można później dodać specjalizacje, grafiki itd.

    def __str__(self):
        return self.user.get_full_name() or self.user.username
