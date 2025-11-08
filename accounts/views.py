from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "accounts/login.html"

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True  # nasz domyślny typ użytkownika
            user.save()
            login(request, user)
            messages.success(request, "Konto zostało utworzone, jesteś zalogowany.")
            return redirect("create_appointment")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})
