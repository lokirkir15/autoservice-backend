from django.db import models

class ServiceType(models.Model):
    name = models.CharField("Nazwa usługi", max_length=100)
    description = models.TextField("Opis", blank=True)
    duration_minutes = models.PositiveIntegerField(
        "Czas trwania [min]",
        help_text="Np. 60 dla godziny, 480 dla całego dnia"
    )
    base_price = models.DecimalField("Cena bazowa", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
