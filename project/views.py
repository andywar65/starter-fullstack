from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from pages.models import Shotgun, ShotgunImage
from users.views import HxTemplateMixin


def check_htmx_request(request):
    """Helper function"""

    if not request.htmx:
        raise Http404("Request without HTMX headers")


def nav_bar(request):
    check_htmx_request(request)
    template_name = "navbar.html"
    context = {"user": request.user}
    return TemplateResponse(request, template_name, context)


class SelectLanguageTemplateView(HxTemplateMixin, TemplateView):
    template_name = "htmx/language_selector.html"


def search_box(request):
    check_htmx_request(request)
    template_name = "htmx/searchbox.html"
    return TemplateResponse(request, template_name, {})


class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)


def search_results(request):
    success = False
    template_name = "search_results.html"
    if request.htmx:
        template_name = "htmx/search_results.html"
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = SearchQuery(request.GET["q"])
        v = SearchVector("url", "title", "content", "sites")
        # search in flatpages
        l_code = f"/{request.LANGUAGE_CODE}/"
        flatpages = FlatPage.objects.filter(url__startswith=l_code).annotate(
            rank=SearchRank(v, q)
        )
        flatpages = flatpages.filter(rank__gt=0.01)
        if flatpages:
            flatpages = flatpages.order_by("-rank")
            success = True
        # search in shotgun articles, no language required
        v = SearchVector("title", "body")
        shots = Shotgun.objects.filter(published=True).annotate(rank=SearchRank(v, q))
        shots = shots.filter(rank__gt=0.01)
        if shots:
            shots = shots.order_by("-rank")
            success = True
        # search in shotgun images, no language required
        v = SearchVector("description")
        images = ShotgunImage.objects.filter(shot__published=True).annotate(
            rank=SearchRank(v, q)
        )
        images = images.filter(rank__gt=0.01)
        if images:
            images = images.order_by("-rank")
            success = True

        return TemplateResponse(
            request,
            template_name,
            {
                "search": request.GET["q"],
                "flatpages": flatpages,
                "shots": shots,
                "images": images,
                "success": success,
            },
        )
    else:
        return TemplateResponse(
            request,
            template_name,
            {
                "success": success,
            },
        )
