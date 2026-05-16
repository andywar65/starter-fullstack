from typing import Any

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.syndication.views import Feed
from django.db.models.query import QuerySet
from django.http.request import HttpRequest as HttpRequest
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.views.generic import DetailView, ListView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.edit import FormView
from filer.models import Image

from .forms import ShotgunCreateForm, StorySelectForm
from .models import Shot2Story, Shotgun, ShotgunImage, Story, default_intro


class ShotgunArchiveIndexView(ArchiveIndexView):
    model = Shotgun
    date_field = "date"
    context_object_name = "shots"
    paginate_by = 6
    allow_empty = True
    template_name = "pages/htmx/shotgun_index.html"

    def get_queryset(self) -> QuerySet[Any]:
        qs = Shotgun.objects.filter(published=True)
        return qs

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        return [self.template_name]


class ShotgunArchiveLimited(ShotgunArchiveIndexView):

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.shot = Shotgun.objects.get(id=kwargs["pk"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        qs = Shotgun.objects.filter(date__lte=self.shot.date, published=True)
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["shot"] = self.shot
        return context

    def get_template_names(self):
        if not self.request.htmx:
            return ["pages/shotgun_index_limited.html"]
        return [self.template_name]


class ShotgunDetailView(DetailView):
    # this view is never used in the project,
    # but is here to show how to use htmx with a DetailView
    model = Shotgun
    context_object_name = "shot"
    template_name = "pages/htmx/shotgun_detail.html"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]


class ShotgunCreateFormView(PermissionRequiredMixin, FormView):
    form_class = ShotgunCreateForm
    template_name = "pages/htmx/shotgun_create.html"
    permission_required = "pages.add_shotgun"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]

    def get_initial(self):
        initial = super().get_initial()
        initial["body"] = default_intro()
        return initial

    def form_valid(self, form):
        # assign Shotgun form fields
        user = self.request.user
        title = form.cleaned_data["title"]
        body = form.cleaned_data["body"]
        # create shotgun
        shot = Shotgun.objects.create(title=title, body=body)
        # create filer image
        image = Image.objects.create(
            owner=user,
            original_filename=slugify(title),
            file=form.cleaned_data["image"],
        )
        # create ShotgunImage
        description = form.cleaned_data["description"]
        img = ShotgunImage(shot_id=shot.id, filer_image=image, description=description)
        img.save()

        return super(ShotgunCreateFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("home")


class ShotgunFeed(Feed):
    title = "digitalkOmiX article Feed"
    link = "/en/articles/feed/"
    description = "Updates on new articles in digitalkOmiX.com"

    def items(self):
        return Shotgun.objects.filter(published=True).order_by("-date")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # Return the first paragraph as description
        return strip_tags(item.body.split("\n")[0])

    def item_link(self, item):
        return item.get_absolute_url()


class StoryListView(ListView):
    model = Story
    template_name = "pages/htmx/story_list.html"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]


class ShotgunStoryListView(ListView):
    model = Shotgun
    context_object_name = "shots"
    paginate_by = 6
    allow_empty = True
    template_name = "pages/htmx/shotgun_story.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.story = Story.objects.get(id=kwargs["pk"])

    def get_queryset(self) -> QuerySet[Any]:
        qs = (
            self.story.shots.all()
            .filter(published=True)
            .order_by("shotgun_story__position")
        )
        return qs

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["story"] = self.story
        return context


class StorySelectFormView(FormView):
    # This view is never used in the project,
    # but is here to show how to use action_with_form in the admin
    form_class = StorySelectForm
    template_name = "pages/admin/story_select.html"

    def form_valid(self, form):
        story = form.cleaned_data["story"]
        # Get articles from queryset in GET and associate them with the selected story
        article_ids = self.request.GET["ids"].split(",")
        articles = Shotgun.objects.filter(id__in=article_ids)
        for article in articles:
            obj, created = Shot2Story.objects.get_or_create(
                shot=article, story=story
            )  # noqa
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("admin:pages_shotgun_changelist")
