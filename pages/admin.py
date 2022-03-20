from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import Logo, FooterLink, HomePage, HomePageCarousel

class LogoAdmin(TranslationAdmin):
    list_display = ('title', 'fb_image')

admin.site.register(Logo, LogoAdmin)

class FooterLinkAdmin(TranslationAdmin):
    list_display = ('title', 'link')

admin.site.register(FooterLink, FooterLinkAdmin)

class HomePageCarouselInline(TranslationTabularInline):
    model = HomePageCarousel
    fields = ('position', 'fb_image', 'description', )
    sortable_field_name = "position"
    extra = 0

class HomePageAdmin(TranslationAdmin):
    list_display = ('__str__', )
    inlines = [ HomePageCarouselInline,  ]

admin.site.register(HomePage, HomePageAdmin)
