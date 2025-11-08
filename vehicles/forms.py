from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "registration_number",
            "vin",
            "make",
            "model",
            "year",
            "current_mileage",
        ]
        labels = {
            "registration_number": "Nr rejestracyjny",
            "vin": "VIN",
            "make": "Marka",
            "model": "Model",
            "year": "Rok produkcji",
            "current_mileage": "Aktualny przebieg",
        }
