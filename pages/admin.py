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

    @admin.action(description=_("Associate selected Articles with a Story"))
    # never used, use action_with_form instead
    def associate_with_story(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            reverse("pages:shotgun_associate") + "?ids=" + ",".join(map(str, selected))
        )

    @action_with_form(
        AssociateWithStoryForm,
        description=_("Associate selected Articles with a Story"),
    )
    def action_associate_with_story(self, request, queryset, data):
        story = data["story"]
        count = 0
        for shot in queryset.reverse():
            if not Shot2Story.objects.filter(shot=shot, story=story).exists():
                Shot2Story.objects.create(shot=shot, story=story, position=count)
                count += 1
        message = _('Added %(count)s Articles to Story "%(story)s".') % {
            "count": count,
            "story": story.title,
        }
        self.message_user(request, message)


class DeleteShotgunActionForm(AdminActionForm):
    # No fields needed

    class Meta:
        list_objects = True
        help_text = _(
            "Are you sure you want to remove all Articles in the selected Stories?"
        )


@admin.register(Story)
class StoryAdmin(AdminActionFormsMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "get_article_count",
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
        "reorder_article_position",
        "action_delete_shotguns",
    ]

    @admin.display(description=_("Articles in Story"))
    def get_article_count(self, obj):
        return obj.story_shotgun.count()

    @admin.action(description=_("Revert Article position in selected Stories"))
    def revert_article_position(self, request, queryset):
        for story in queryset:
            last_position = story.story_shotgun.count()
            if last_position:
                for shot2story in story.story_shotgun.all():
                    shot2story.position = last_position - 1
                    shot2story.save(update_fields=["position"])
                    last_position -= 1
        self.message_user(request, _("Reverted Article positions in selected Stories."))

    @admin.action(description=_("Reorder Article position in selected Stories"))
    def reorder_article_position(self, request, queryset):
        for story in queryset:
            last_position = story.story_shotgun.count()
            if last_position:
                for shot2story in story.story_shotgun.all().order_by("shot"):
                    shot2story.position = last_position - 1
                    shot2story.save(update_fields=["position"])
                    last_position -= 1
        self.message_user(
            request, _("Reordered Article positions in selected Stories.")
        )

    @action_with_form(
        DeleteShotgunActionForm,
        description=_("Remove Articles in selected Stories"),
    )
    def action_delete_shotguns(self, request, queryset, data):
        for story in queryset:
            story.story_shotgun.all().delete()
        message = _("Removed Articles in %(count)s Stories.") % {
            "count": queryset.count(),
        }
        self.message_user(request, message)
