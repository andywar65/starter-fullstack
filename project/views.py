from django import forms
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from pages.models import Logo

class HomePageTemplateView(TemplateView):
    template_name = 'base_menu.html'

class SelectLanguageTemplateView(TemplateView):

    def get_template_names(self):
        if self.request.htmx:
            return ['htmx/language_selector.html']
        else:
            return ['language_selector.html']

class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)

def search_results(request):
    success = False
    if request.htmx:
        template = 'htmx/search_results.html'
    else:
        template = 'search_results.html'
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = SearchQuery(request.GET['q'])

        #search in articles example
        #v = SearchVector('title', 'intro', 'body')
        #articles = Article.objects.annotate(rank=SearchRank(v, q))
        #articles = articles.filter(rank__gt=0.01)
        #if articles:
            #articles = articles.order_by('-rank')
            #success = True

        return render(request, template,
            {'search': request.GET['q'],
            'success': success})
    else:
        return render(request, template, {'success': success, })
