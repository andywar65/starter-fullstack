from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_admin_action_forms import (
    AdminActionForm,
    AdminActionFormsMixin,
    action_with_form,
)

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


class AssociateWithStoryForm(AdminActionForm):
    story = forms.ModelChoiceField(
        queryset=Story.objects.all(),
        required=True,
        label=_("Story to associate with"),
    )


@admin.register(Shotgun)
class ShotgunAdmin(AdminActionFormsMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "date",
        "published",
    )
    list_editable = ("published",)
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
    actions = [
        # "associate_with_story",
        "action_associate_with_story",
    ]

    @admin.action(description=_("Associate selected articles with a story"))
    # never used, use action_with_form instead
    def associate_with_story(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            reverse("pages:shotgun_associate") + "?ids=" + ",".join(map(str, selected))
        )

    @action_with_form(
        AssociateWithStoryForm,
        description=_("Associate selected articles with a story"),
    )
    def action_associate_with_story(self, request, queryset, data):
        story = data["story"]
        count = 0
        for shot in queryset.reverse():
            obj, created = Shot2Story.objects.get_or_create(
                shot=shot, story=story, position=count
            )  # noqa
            if created:
                count += 1
        self.message_user(request, f"Added {count} articles to story '{story.title}'.")


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
    actions = [
        "revert_article_position",
    ]

    @admin.action(description=_("Revert article position in Story"))
    def revert_article_position(self, request, queryset):
        for story in queryset:
            last_position = story.story_shotgun.last().position
            for shot2story in story.story_shotgun.all():
                shot2story.position = last_position
                shot2story.save(update_fields=["position"])
                last_position -= 1
        self.message_user(request, "Reverted article positions in selected stories.")
