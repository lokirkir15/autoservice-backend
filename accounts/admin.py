from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # dodajemy nasze pola do standardowego UserAdmin
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Dodatkowe informacje', {
            'fields': ('phone_number', 'is_customer', 'is_technician'),
        }),
    )

    list_display = ('username', 'email', 'phone_number', 'is_customer', 'is_technician', 'is_staff')
    list_filter = ('is_customer', 'is_technician', 'is_staff', 'is_superuser', 'is_active')
