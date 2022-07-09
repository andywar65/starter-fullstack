from django import forms
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render
from django.views.generic import TemplateView

from buildings.models import Journal
from djeotree.models import Element
from pages.models import Article
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
        # search in articles
        v = SearchVector("title", "intro", "body")
        articles = Article.objects.annotate(rank=SearchRank(v, q))
        articles = articles.filter(rank__gt=0.01)
        if articles:
            articles = articles.order_by("-rank")
            success = True
        # search in journals
        jours = Journal.objects.annotate(rank=SearchRank(v, q))
        jours = jours.filter(rank__gt=0.01)
        if jours:
            jours = jours.order_by("-rank")
            success = True
        # search in djeotree elements
        v = SearchVector("intro", "body")
        elements = Element.objects.annotate(rank=SearchRank(v, q))
        elements = elements.filter(rank__gt=0.01)
        if elements:
            elements = elements.order_by("-rank")
            success = True

        return render(
            request,
            template,
            {
                "search": request.GET["q"],
                "articles": articles,
                "jours": jours,
                "elements": elements,
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
