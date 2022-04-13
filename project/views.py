from django import forms
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render
from django.views.generic import TemplateView

from pages.models import Article
from portfolio.models import Project
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
        # search in projects
        projects = Project.objects.annotate(rank=SearchRank(v, q))
        projects = projects.filter(rank__gt=0.01)
        if projects:
            projects = projects.order_by("-rank")
            success = True

        return render(
            request,
            template,
            {
                "search": request.GET["q"],
                "articles": articles,
                "projects": projects,
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
