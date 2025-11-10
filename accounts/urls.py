from django.urls import path
from .views import UserLoginView, logout_view, register, home

urlpatterns = [
    path("", home, name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
]
