from typing import Any

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.request import HttpRequest as HttpRequest
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView
from django.views.generic.dates import (
    ArchiveIndexView,
    DayArchiveView,
    MonthArchiveView,
    YearArchiveView,
)
from django.views.generic.edit import FormView
from filer.models import Image

from users.views import HxTemplateMixin

from .forms import ShotgunCreateForm
from .models import Article, HomePage, Shotgun, ShotgunImage


class HxPageTemplateMixin:
    """Switches template depending on request.htmx and pagination"""

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        elif "page" in self.request.GET:
            return ["pages/includes/infinite_scroll.html"]
        else:
            return [self.template_name]


class HomePageTemplateView(HxTemplateMixin, TemplateView):
    template_name = "pages/htmx/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = HomePage.objects.first()
        if not context["page"]:
            raise Http404(_("No Home Pages available"))
        # we add this context to feed the gallery
        context["main_gal_slug"] = get_random_string(7)
        context["title"] = context["page"].title
        # context for the page
        context["images"] = context["page"].homepage_carousel.all()
        context["articles"] = Article.objects.all()[:6]
        return context


class ArticleArchiveIndexView(HxPageTemplateMixin, ArchiveIndexView):
    model = Article
    date_field = "date"
    context_object_name = "articles"
    paginate_by = 6
    allow_empty = True
    template_name = "pages/htmx/article_index.html"


class ShotgunArchiveIndexView(ArchiveIndexView):
    model = Shotgun
    date_field = "date"
    context_object_name = "shots"
    paginate_by = 6
    allow_empty = True
    template_name = "pages/htmx/shotgun_index.html"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        elif "page" in self.request.GET:
            return ["pages/includes/infinite_shotgun.html"]
        else:
            return [self.template_name]


class ShotgunArchiveLimited(ShotgunArchiveIndexView):

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.shot = Shotgun.objects.get(id=kwargs["pk"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        qs = Shotgun.objects.filter(date__lte=self.shot.date)
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["shot"] = self.shot
        return context


class ArticleYearArchiveView(HxPageTemplateMixin, YearArchiveView):
    model = Article
    date_field = "date"
    make_object_list = True
    context_object_name = "articles"
    paginate_by = 6
    year_format = "%Y"
    allow_empty = True
    template_name = "pages/htmx/article_index.html"


class ArticleMonthArchiveView(HxPageTemplateMixin, MonthArchiveView):
    model = Article
    date_field = "date"
    context_object_name = "articles"
    paginate_by = 6
    year_format = "%Y"
    month_format = "%m"
    allow_empty = True
    template_name = "pages/htmx/article_index.html"


class ArticleDayArchiveView(HxPageTemplateMixin, DayArchiveView):
    model = Article
    date_field = "date"
    context_object_name = "articles"
    paginate_by = 6
    year_format = "%Y"
    month_format = "%m"
    day_format = "%d"
    allow_empty = True
    template_name = "pages/htmx/article_index.html"


class ArticleDetailView(HxTemplateMixin, DetailView):
    model = Article
    context_object_name = "article"
    slug_field = "slug"
    template_name = "pages/htmx/article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # we add this context to feed the gallery
        context["main_gal_slug"] = get_random_string(7)
        context["title"] = context["article"].title
        # context for the post
        context["images"] = context["article"].article_carousel.all()
        return context


class ShotgunDetailView(DetailView):
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
        return reverse("shotgun_index")
