from django.contrib import admin
from .models import TireSet

@admin.register(TireSet)
class TireSetAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'customer', 'vehicle', 'is_in_storage', 'location')
    list_filter = ('is_in_storage',)
    search_fields = ('identifier', 'customer__username', 'vehicle__registration_number')
