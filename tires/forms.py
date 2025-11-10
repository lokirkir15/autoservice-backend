from django import forms
from .models import TireSet
from accounts.models import User


class TireSetForm(forms.ModelForm):
    class Meta:
        model = TireSet
        fields = [
            "identifier",
            "customer",
            "vehicle",
            "description",
            "location",
            "is_in_storage",
        ]
        labels = {
            "identifier": "ID kompletu",
            "customer": "Klient",
            "vehicle": "Pojazd",
            "description": "Opis",
            "location": "Lokalizacja w magazynie",
            "is_in_storage": "Aktualnie w magazynie",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filtrowanie klientów (opcjonalnie – tylko tacy, co są klientami)
        self.fields["customer"].queryset = User.objects.filter(is_customer=True)
