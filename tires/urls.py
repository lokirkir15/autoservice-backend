from django.urls import path
from . import views

urlpatterns = [
    # widok klienta
    path("my/", views.my_tires, name="my_tires"),

    # magazyn (panel staff)
    path("warehouse/", views.warehouse_list, name="warehouse_list"),
    path("warehouse/new/", views.warehouse_create, name="warehouse_create"),
    path("warehouse/<int:pk>/edit/", views.warehouse_update, name="warehouse_update"),
    path("warehouse/<int:pk>/delete/", views.warehouse_delete, name="warehouse_delete"),
]
