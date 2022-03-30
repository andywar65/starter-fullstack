from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def create_home_page(sender, **kwargs):
    from django.contrib.sites.models import Site

    from .models import HomePage

    hp = HomePage.objects.all()
    if not hp:
        current_site = Site.objects.get_current()
        if current_site.name:
            hp_title = current_site.name
        else:
            hp_title = _("Home page")
        HomePage.objects.create(title=hp_title)


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"

    def ready(self):
        post_migrate.connect(create_home_page, sender=self)
