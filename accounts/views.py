from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "accounts/login.html"

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    User = get_user_model()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # domyślnie klient
            user.is_customer = True

            # 👇 MAGICZNY FRAGMENT: jeśli NIE ma jeszcze żadnego superusera,
            # ten użytkownik zostanie administratorem
            if not User.objects.filter(is_superuser=True).exists():
                user.is_staff = True
                user.is_superuser = True
                user.is_customer = False  # opcjonalnie, żeby admin nie był "klientem"

            user.save()
            login(request, user)
            messages.success(request, "Konto zostało utworzone, jesteś zalogowany.")
            return redirect("create_appointment")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})
