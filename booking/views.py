from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from vehicles.models import Vehicle

from .forms import AppointmentForm
from .models import Appointment
from .utils import (
    is_slot_available,
    get_available_technician,
    get_available_workstation,
)


@login_required
def create_appointment(request):
    if not Vehicle.objects.filter(owner=request.user).exists():
        messages.info(request, "Najpierw dodaj pojazd, aby umówić wizytę.")
        return redirect("vehicle_create")
    
    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            vehicle = form.cleaned_data["vehicle"]
            service_type = form.cleaned_data["service_type"]
            start = form.cleaned_data["start"]
            duration = timedelta(minutes=service_type.duration_minutes)
            end = start + duration

            if not is_slot_available(start, service_type):
                messages.error(request, "Wybrany termin jest już zajęty. Wybierz inny.")
            else:
                technician = get_available_technician(start, duration)
                workstation = get_available_workstation(start, duration)

                if technician is None or workstation is None:
                    messages.error(
                        request,
                        "Brak wolnego technika lub stanowiska w tym terminie."
                    )
                else:
                    Appointment.objects.create(
                        customer=request.user,
                        vehicle=vehicle,
                        service_type=service_type,
                        start=start,
                        end=end,
                        assigned_technician=technician,
                        workstation=workstation,
                    )
                    messages.success(request, "Wizyta została umówiona.")
                    return redirect("appointment_success")
    else:
        form = AppointmentForm(user=request.user)

    return render(request, "booking/appointment_form.html", {"form": form})


@login_required
def appointment_success(request):
    return render(request, "booking/appointment_success.html")

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        customer=request.user
    ).order_by('-start')
    return render(
        request,
        "booking/my_appointments.html",
        {"appointments": appointments}
    )