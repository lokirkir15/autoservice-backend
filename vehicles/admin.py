from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'make', 'model', 'owner')
    search_fields = ('registration_number', 'vin', 'make', 'model', 'owner__username')
