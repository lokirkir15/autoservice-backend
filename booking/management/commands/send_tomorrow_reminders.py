from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from booking.models import Appointment
from booking.utils import send_appointment_reminder


class Command(BaseCommand):
    help = "Wysyła przypomnienia o jutrzejszych wizytach (tylko dla zaplanowanych, bez wysłanego przypomnienia)."

    def handle(self, *args, **options):
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        qs = Appointment.objects.filter(
            status=Appointment.Status.SCHEDULED,
            start__date=tomorrow,
            reminder_sent=False,
        )

        count = qs.count()
        if count == 0:
            self.stdout.write("Brak wizyt do przypomnienia na jutro.")
            return

        self.stdout.write(f"Znaleziono {count} wizyt na jutro. Wysyłam przypomnienia...")

        for appointment in qs:
            send_appointment_reminder(appointment)
            appointment.reminder_sent = True
            appointment.save(update_fields=["reminder_sent"])
            self.stdout.write(
                f"- {appointment.id}: {appointment.customer} – {appointment.start}"
            )

        self.stdout.write(self.style.SUCCESS("Zakończono wysyłanie przypomnień."))
