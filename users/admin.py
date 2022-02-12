from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (User, Profile, )

class UserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'is_superuser')
    list_editable = ('is_staff', 'is_active')

admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', )
