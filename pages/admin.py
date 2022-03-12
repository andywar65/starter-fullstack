from django.contrib import admin

from .models import ImageData, Logo, FooterLink

@admin.register(ImageData)
class ImageDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'original', 'date')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'original', 'date', ),
        }),
        )

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')
