from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin

from .models import (User, Profile, UserMessage )

class UserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'is_superuser')
    list_editable = ('is_staff', 'is_active')

admin.site.register(User, UserAdmin)

class ProfileAdmin(TranslationAdmin):
    list_display = ('get_full_name', )
    exclude = ('temp_image', )

admin.site.register(Profile, ProfileAdmin)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', )
