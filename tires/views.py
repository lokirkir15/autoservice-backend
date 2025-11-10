from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import TireSet
from .forms import TireSetForm

@staff_member_required
def warehouse_list(request):
    tire_sets = (
        TireSet.objects
        .select_related("customer", "vehicle")
        .order_by("identifier")
    )
    return render(
        request,
        "tires/warehouse_list.html",
        {"tire_sets": tire_sets},
    )

@staff_member_required
def warehouse_create(request):
    if request.method == "POST":
        form = TireSetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Komplet opon został dodany do magazynu.")
            return redirect("warehouse_list")
    else:
        form = TireSetForm()

    return render(
        request,
        "tires/warehouse_form.html",
        {"form": form, "title": "Dodaj komplet opon"},
    )

@staff_member_required
def warehouse_update(request, pk):
    tire_set = get_object_or_404(TireSet, pk=pk)

    if request.method == "POST":
        form = TireSetForm(request.POST, instance=tire_set)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane kompletu opon zostały zaktualizowane.")
            return redirect("warehouse_list")
    else:
        form = TireSetForm(instance=tire_set)

    return render(
        request,
        "tires/warehouse_form.html",
        {"form": form, "title": "Edytuj komplet opon"},
    )

@staff_member_required
def warehouse_delete(request, pk):
    tire_set = get_object_or_404(TireSet, pk=pk)

    if request.method == "POST":
        tire_set.delete()
        messages.success(request, "Komplet opon został usunięty z magazynu.")
        return redirect("warehouse_list")

    return render(
        request,
        "tires/warehouse_confirm_delete.html",
        {"tire_set": tire_set},
    )

@login_required
def my_tires(request):
    tire_sets = (
        TireSet.objects
        .filter(customer=request.user)
        .select_related("vehicle")
        .order_by("identifier")
    )
    return render(
        request,
        "tires/my_tires.html",
        {"tire_sets": tire_sets},
    )
