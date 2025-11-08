from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.create_appointment, name="create_appointment"),
    path("success/", views.appointment_success, name="appointment_success"),
    path("my/", views.my_appointments, name="my_appointments"),
]
