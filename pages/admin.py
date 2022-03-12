from django.contrib import admin

from .models import ImageData, Logo, FooterLink, HomePage

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
    list_display = ('title', 'link')

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
