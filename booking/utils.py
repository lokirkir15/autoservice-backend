from datetime import timedelta

from django.conf import settings

from accounts.models import User
from workshop.models import Workstation
from .models import Appointment


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
