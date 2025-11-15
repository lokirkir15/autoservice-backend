from django.urls import path
from .views import UserLoginView, logout_view, register, home, about

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),  # <--- nowa trasa
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
]
