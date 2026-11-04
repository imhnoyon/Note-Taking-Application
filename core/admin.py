from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username","first_name","last_name","email","role","is_staff","is_active")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title","description","created_at","updated_at")