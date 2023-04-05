from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationTabularInline

from .models import Profile, User, UserMessage


class ProfileAdmin(TranslationTabularInline):
    model = Profile
    exclude = ("temp_image",)
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "is_staff", "is_active", "is_superuser")
    list_editable = ("is_staff", "is_active")
    inlines = [
        ProfileAdmin,
    ]


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subject",
    )
