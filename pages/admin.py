from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from tinymce.widgets import TinyMCE

from .models import (
    Article,
    ArticleCarousel,
    FooterLink,
    HomePage,
    HomePageCarousel,
    Logo,
)


@admin.register(Logo)
class LogoAdmin(TranslationAdmin):
    list_display = ("title", "fb_image")


@admin.register(FooterLink)
class FooterLinkAdmin(TranslationAdmin):
    list_display = ("title", "link")


class HomePageCarouselInline(TranslationTabularInline):
    model = HomePageCarousel
    fields = (
        "position",
        "fb_image",
        "description",
    )
    sortable_field_name = "position"
    extra = 0


@admin.register(HomePage)
class HomePageAdmin(TranslationAdmin):
    list_display = ("__str__",)
    inlines = [
        HomePageCarouselInline,
    ]


class TinyMCEFlatPageAdmin(FlatPageAdmin):
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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "content":
            return db_field.formfield(
                widget=TinyMCE(
                    attrs={"cols": 80, "rows": 30},
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)


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

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "intro", "date"),
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
