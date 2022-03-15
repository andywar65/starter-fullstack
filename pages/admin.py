from django.contrib import admin

from .models import Logo, FooterLink, HomePage, HomePageCarousel

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('title', 'fb_image')

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')

class HomePageCarouselInline(admin.TabularInline):
    model = HomePageCarousel
    fields = ('position', 'fb_image', 'description', )
    sortable_field_name = "position"
    extra = 0

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    inlines = [ HomePageCarouselInline,  ]
