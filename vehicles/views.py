from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Vehicle
from .forms import VehicleForm

@login_required
def my_vehicles(request):
    vehicles = Vehicle.objects.filter(owner=request.user).order_by("registration_number")
    return render(request, "vehicles/my_vehicles.html", {"vehicles": vehicles})


@login_required
def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, "Pojazd został dodany.")
            return redirect("my_vehicles")
    else:
        form = VehicleForm()

    return render(request, "vehicles/vehicle_form.html", {"form": form, "title": "Dodaj pojazd"})


@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)

    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane pojazdu zostały zaktualizowane.")
            return redirect("my_vehicles")
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, "vehicles/vehicle_form.html", {"form": form, "title": "Edytuj pojazd"})


@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)

    if request.method == "POST":
        vehicle.delete()
        messages.success(request, "Pojazd został usunięty.")
        return redirect("my_vehicles")

    return render(request, "vehicles/vehicle_confirm_delete.html", {"vehicle": vehicle})
