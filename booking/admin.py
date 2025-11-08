from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'service_type', 'start', 'status', 'assigned_technician', 'workstation')
    list_filter = ('status', 'service_type')
    search_fields = ('vehicle__registration_number', 'customer__username')
    list_select_related = ('vehicle', 'service_type', 'customer', 'assigned_technician', 'workstation')
