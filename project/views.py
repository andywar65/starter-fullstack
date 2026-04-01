from django import forms
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render
from django.views.generic import TemplateView

from pages.models import Shotgun
from users.views import HxTemplateMixin


class SelectLanguageTemplateView(HxTemplateMixin, TemplateView):
    template_name = "htmx/language_selector.html"


class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)


def search_results(request):
    success = False
    if request.htmx:
        template = "htmx/search_results.html"
    else:
        template = "search_results.html"
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = SearchQuery(request.GET["q"])
        # search in shotgun articles
        v = SearchVector("title", "body")
        shots = Shotgun.objects.annotate(rank=SearchRank(v, q))
        shots = shots.filter(rank__gt=0.01)
        if shots:
            shots = shots.order_by("-rank")
            success = True

        return render(
            request,
            template,
            {
                "search": request.GET["q"],
                "shots": shots,
                "success": success,
            },
        )
    else:
        return render(
            request,
            template,
            {
                "success": success,
            },
        )
