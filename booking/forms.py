from django import forms
from django.utils import timezone

from vehicles.models import Vehicle
from services.models import ServiceType
from .utils import is_within_working_hours

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

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        service_type = cleaned_data.get("service_type")

        if not start or not service_type:
            return cleaned_data

        # Upewniamy się, że start jest "aware" i w lokalnej strefie
        if timezone.is_naive(start):
            start_aware = timezone.make_aware(start, timezone.get_current_timezone())
        else:
            start_aware = start

        now = timezone.now()  # też aware

        # 1) Zakaz umawiania wizyt w przeszłości
        if start_aware < now:
            self.add_error("start", "Nie można umawiać wizyt w przeszłości.")
            return cleaned_data

        # 2) Godziny pracy, dni tygodnia – użyjemy funkcji z utils
        ok, msg = is_within_working_hours(start_aware, service_type.duration_minutes)
        if not ok:
            self.add_error("start", msg)

        return cleaned_data