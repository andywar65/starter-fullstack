from django.contrib.flatpages.models import FlatPage
from django.contrib.sitemaps import Sitemap

class FlatPageSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return FlatPage.objects.all()
