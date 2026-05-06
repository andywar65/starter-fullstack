from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

# from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from .models import FooterLink, Logo, Shot2Story, Shotgun, ShotgunImage, Story


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ("title", "image")


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "link")


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


class ShotgunImageInline(admin.TabularInline):
    model = ShotgunImage
    fields = (
        "position",
        "description",
        "filer_image",
    )
    extra = 0


class Shot2StoryInline(admin.TabularInline):
    model = Shot2Story
    fields = ("story",)
    extra = 0


class Story2ShotInline(admin.TabularInline):
    model = Shot2Story
    fields = ("shot", "position")
    extra = 0


@admin.register(Shotgun)
class ShotgunAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date",
        "published",
    )
    fields = (
        "published",
        "toot",
        "title",
        "slug",
        "body",
        "date",
    )
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ShotgunImageInline,
        Shot2StoryInline,
    ]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
    fields = (
        "title",
        "slug",
        "description",
    )
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        Story2ShotInline,
    ]
