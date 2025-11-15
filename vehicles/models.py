from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    registration_number = models.CharField("Nr rejestracyjny", max_length=20, unique=True)
    vin = models.CharField("VIN", max_length=17, blank=True)
    make = models.CharField("Marka", max_length=50)
    model = models.CharField("Model", max_length=50)
    year = models.PositiveIntegerField("Rok", null=True, blank=True)
    current_mileage = models.PositiveIntegerField("Aktualny przebieg", null=True, blank=True)
    photo = models.ImageField(
        "Zdjęcie",
        upload_to="vehicles/",
        blank=True,
        null=True,
        help_text="Opcjonalne zdjęcie pojazdu",
    )

    def __str__(self):
        return f"{self.registration_number} – {self.make} {self.model}"
