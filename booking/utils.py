import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from accounts.models import User
from workshop.models import Workstation
from .models import Appointment

logger = logging.getLogger(__name__)

def get_max_parallel_jobs() -> int:
    """
    Maksymalna liczba równoległych zleceń:
    min(liczba aktywnych stanowisk, liczba aktywnych techników).
    """
    technicians = User.objects.filter(is_technician=True, is_active=True).count()
    workstations = Workstation.objects.filter(is_active=True).count()
    if technicians == 0 or workstations == 0:
        return 0
    return min(technicians, workstations)


def is_slot_available(start, service_type) -> bool:
    """
    Czy w danym oknie czasowym jest jeszcze miejsce na kolejne zlecenie?
    """
    duration = timedelta(minutes=service_type.duration_minutes)
    end = start + duration
    max_jobs = get_max_parallel_jobs()
    if max_jobs == 0:
        return False

    overlapping = Appointment.objects.filter(
        status__in=[Appointment.Status.SCHEDULED, Appointment.Status.IN_PROGRESS],
        start__lt=end,
        end__gt=start,
    ).count()

    return overlapping < max_jobs


def get_available_technician(start, duration: timedelta):
    """
    Zwraca pierwszego technika, który nie ma w tym czasie zlecenia.
    """
    end = start + duration
    technicians = User.objects.filter(is_technician=True, is_active=True)

    for tech in technicians:
        has_overlap = tech.assigned_appointments.filter(
            status__in=[Appointment.Status.SCHEDULED, Appointment.Status.IN_PROGRESS],
            start__lt=end,
            end__gt=start,
        ).exists()
        if not has_overlap:
            return tech
    return None


def get_available_workstation(start, duration: timedelta):
    """
    Zwraca pierwsze stanowisko, które nie ma w tym czasie zlecenia.
    """
    end = start + duration
    workstations = Workstation.objects.filter(is_active=True)

    for ws in workstations:
        has_overlap = ws.appointment_set.filter(
            status__in=[Appointment.Status.SCHEDULED, Appointment.Status.IN_PROGRESS],
            start__lt=end,
            end__gt=start,
        ).exists()
        if not has_overlap:
            return ws
    return None

def _send_email(subject: str, message: str, recipient: str) -> None:
    """
    Wspólny helper do wysyłania maili. Nie podnosi wyjątków, zamiast tego loguje błąd.
    """
    if not recipient:
        return

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=True,  # a i tak trzymamy to w try/except
        )
    except Exception as e:
        logger.exception("Błąd podczas wysyłania maila: %s", e)

def send_appointment_confirmation(appointment: Appointment) -> None:
    customer = appointment.customer

    if not customer.email:
        return

    subject = "Potwierdzenie wizyty w serwisie MechAuto"
    start_str = appointment.start.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M")

    message = (
        f"Cześć {customer.username},\n\n"
        f"Twoja wizyta została umówiona.\n\n"
        f"Data i godzina: {start_str}\n"
        f"Pojazd: {appointment.vehicle}\n"
        f"Usługa: {appointment.service_type}\n\n"
        f"Do zobaczenia w serwisie!"
    )

    _send_email(subject, message, customer.email)

def send_appointment_reminder(appointment: Appointment) -> None:
    """
    Wysyła przypomnienie o wizycie dzień wcześniej.
    """
    customer = appointment.customer

    if not customer.email:
        return

    subject = "Przypomnienie o jutrzejszej wizycie w serwisie MechAuto"
    start_local = appointment.start.astimezone(timezone.get_current_timezone())
    start_str = start_local.strftime("%Y-%m-%d %H:%M")

    message = (
        f"Cześć {customer.username},\n\n"
        f"Przypominamy o Twojej wizycie w serwisie MechAuto.\n\n"
        f"Data i godzina: {start_str}\n"
        f"Pojazd: {appointment.vehicle}\n"
        f"Usługa: {appointment.service_type}\n\n"
        f"Jeśli nie możesz przyjechać, prosimy o kontakt z serwisem.\n"
    )

    _send_email(subject, message, customer.email)
