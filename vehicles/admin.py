from django.contrib import admin
from django.utils.html import format_html
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "make", "model", "year", "owner", "photo_thumb")
    list_filter = ("year",)
    search_fields = ("registration_number", "vin", "make", "model")

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.photo.url)
        return "-"
    photo_thumb.short_description = "Zdjęcie"
