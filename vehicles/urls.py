from django.urls import path
from . import views

urlpatterns = [
    path("my/", views.my_vehicles, name="my_vehicles"),
    path("new/", views.vehicle_create, name="vehicle_create"),
    path("<int:pk>/edit/", views.vehicle_update, name="vehicle_update"),
    path("<int:pk>/delete/", views.vehicle_delete, name="vehicle_delete"),
    path("<int:pk>/history/", views.vehicle_history, name="vehicle_history"),
]
