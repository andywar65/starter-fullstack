from django.http import Http404
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView
from django.views.generic.dates import (
    ArchiveIndexView,
    DayArchiveView,
    MonthArchiveView,
    YearArchiveView,
)

from users.views import HxTemplateMixin

from .models import Article, HomePage


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


class ArticleArchiveIndexView(HxTemplateMixin, ArchiveIndexView):
    model = Article
    date_field = "date"
    allow_future = True
    context_object_name = "articles"
    paginate_by = 12
    allow_empty = True
    template_name = "pages/htmx/article_index.html"


class ArticleYearArchiveView(YearArchiveView):
    model = Article
    make_object_list = True
    date_field = "date"
    allow_future = True
    context_object_name = "articles"
    paginate_by = 12
    year_format = "%Y"
    allow_empty = True


class ArticleMonthArchiveView(MonthArchiveView):
    model = Article
    date_field = "date"
    allow_future = True
    context_object_name = "articles"
    year_format = "%Y"
    month_format = "%m"
    allow_empty = True


class ArticleDayArchiveView(DayArchiveView):
    model = Article
    date_field = "date"
    allow_future = True
    context_object_name = "articles"
    year_format = "%Y"
    month_format = "%m"
    day_format = "%d"
    allow_empty = True


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
