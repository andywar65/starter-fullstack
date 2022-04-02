from django.http import Http404
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from users.views import HxTemplateMixin

from .models import HomePage


class HomePageTemplateView(HxTemplateMixin, TemplateView):
    template_name = "pages/htmx/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = HomePage.objects.first()
        if not context["page"]:
            raise Http404(_("No Home Pages available"))
        # we add this context to feed the standard gallery
        context["main_gal_slug"] = get_random_string(7)
        context["title"] = context["page"].title
        # context for the page
        context["images"] = context["page"].homepage_carousel.all()
        return context
