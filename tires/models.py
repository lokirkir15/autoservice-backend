from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

class TireSet(models.Model):
    identifier = models.CharField(
        "Identyfikator kompletu",
        max_length=50,
        unique=True,
        help_text="Numer naklejony na komplet/regal"
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tire_sets'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tire_sets'
    )
    description = models.CharField(
        "Opis",
        max_length=200,
        blank=True,
        help_text="Np. 205/55 R16 zimowe"
    )
    location = models.CharField(
        "Miejsce składowania",
        max_length=100,
        blank=True,
        help_text="Regał / sektor / półka"
    )
    is_in_storage = models.BooleanField("W magazynie", default=True)

    def __str__(self):
        return f"{self.identifier} – {self.customer}"
