from django.db import models
from django.conf import settings
from vehicles.models import Vehicle
from services.models import ServiceType
from workshop.models import Workstation

class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Zaplanowana"
        IN_PROGRESS = "in_progress", "W realizacji"
        DONE = "done", "Zakończona"
        CANCELLED = "cancelled", "Anulowana"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    start = models.DateTimeField("Początek")
    end = models.DateTimeField("Koniec")
    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )

    assigned_technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_appointments'
    )
    workstation = models.ForeignKey(
        Workstation,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    mileage_at_service = models.PositiveIntegerField("Przebieg przy wizycie", null=True, blank=True)
    notes = models.TextField("Notatki", blank=True)

    notes = models.TextField("Notatki", blank=True)

    reminder_sent = models.BooleanField(
        "Przypomnienie wysłane",
        default=False,
        help_text="Czy wysłano już przypomnienie o tej wizycie"
    )

    def __str__(self):
        return f"{self.vehicle} – {self.service_type} – {self.start}"
