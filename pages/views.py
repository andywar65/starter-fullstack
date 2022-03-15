from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView
from django.utils.crypto import get_random_string

from .models import HomePage

class HomePageTemplateView(TemplateView):
    template_name = 'pages/home.html'

    def get_template_names(self):
        if self.request.htmx:
            return [self.template_name.replace('pages/', 'pages/htmx/')]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = HomePage.objects.first()
        if not context['page']:
            raise Http404(_("No Home Pages available"))
        #we add this context to feed the standard gallery
        context['main_gal_slug'] = get_random_string(7)
        context['title'] = context['page'].title
        #context for the page
        context['images'] = context['page'].homepage_carousel.all()
        return context
