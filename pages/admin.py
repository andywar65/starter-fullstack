from django.contrib import admin

from .models import ImageData

@admin.register(ImageData)
class ImageDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'original', 'date')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'original', 'date', ),
        }),
        )
