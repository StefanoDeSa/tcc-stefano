from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff", "is_active", "mfa_enabled"]
    fieldsets = UserAdmin.fieldsets + (
        ("Autenticação de Dois Fatores", {"fields": ("mfa_secret", "mfa_enabled")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Autenticação de Dois Fatores", {"fields": ("mfa_enabled",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
