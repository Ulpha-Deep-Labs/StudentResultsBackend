from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUSerChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUSerChangeForm
    model = CustomUser

    list_display = [
                    "username",
                    "email",
                    "role",
                    "is_staff"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role", )}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("role",)}),)

admin.site.register(CustomUser, CustomUserAdmin)
