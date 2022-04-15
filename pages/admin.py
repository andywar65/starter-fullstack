from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import (
    Article,
    ArticleCarousel,
    FooterLink,
    HomePage,
    HomePageCarousel,
    Logo,
)


class LogoAdmin(TranslationAdmin):
    list_display = ("title", "fb_image")


admin.site.register(Logo, LogoAdmin)


class FooterLinkAdmin(TranslationAdmin):
    list_display = ("title", "link")


admin.site.register(FooterLink, FooterLinkAdmin)


class HomePageCarouselInline(TranslationTabularInline):
    model = HomePageCarousel
    fields = (
        "position",
        "fb_image",
        "description",
    )
    sortable_field_name = "position"
    extra = 0


class HomePageAdmin(TranslationAdmin):
    list_display = ("__str__",)
    inlines = [
        HomePageCarouselInline,
    ]

    class Media:
        js = [
            "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
            "/static/js/tinymce_setup.js",
        ]


admin.site.register(HomePage, HomePageAdmin)


class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {"fields": ("url", "title", "content", "sites")}),
        (
            _("Advanced options"),
            {
                "fields": (
                    # 'enable_comments',
                    "registration_required",
                    "template_name",
                ),
            },
        ),
    )

    class Media:
        js = [
            "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
            "/static/js/tinymce_setup.js",
        ]


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


class ArticleCarouselInline(TranslationTabularInline):
    model = ArticleCarousel
    fields = (
        "position",
        "fb_image",
        "description",
    )
    sortable_field_name = "position"
    extra = 0


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ("title", "date", "author")
    search_fields = ("title", "date", "intro")
    inlines = [
        ArticleCarouselInline,
    ]

    class Media:
        js = [
            "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
            "/static/js/tinymce_setup.js",
        ]

    fieldsets = (
        (
            None,
            {
                "fields": ("slug", "title", "date", "intro"),
            },
        ),
        (
            _("Text"),
            {
                "classes": ("grp-collapse",),
                "fields": ("body",),
            },
        ),
        (
            None,
            {
                "fields": ("author",),
            },
        ),
    )
