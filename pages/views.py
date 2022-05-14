from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView
from django.views.generic.dates import (
    ArchiveIndexView,
    DayArchiveView,
    MonthArchiveView,
    YearArchiveView,
)
from django.views.generic.edit import FormView

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
        title = form.cleaned_data["title"]
        body = form.cleaned_data["body"]
        shot = Shotgun.objects.create(title=title, body=body)
        # assign ShotgunImage form fields
        image = form.cleaned_data["image"]
        description = form.cleaned_data["description"]
        img = ShotgunImage(shot_id=shot.id, image=image, description=description)
        img.save()

        return super(ShotgunCreateFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("shotgun_index")
