from django import forms

from vehicles.models import Vehicle
from services.models import ServiceType


class AppointmentForm(forms.Form):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.none(), label="Pojazd")
    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        label="Usługa"
    )
    start = forms.DateTimeField(
        label="Data i godzina rozpoczęcia",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["vehicle"].queryset = Vehicle.objects.filter(owner=user)
        else:
            self.fields["vehicle"].queryset = Vehicle.objects.all()
