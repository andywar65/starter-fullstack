from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from filebrowser.sites import site

from pages.views import HomePageTemplateView
from users.views import (
    ContactFormView,
    HTMXLoginView,
    HTMXLogoutView,
    HTMXSignupView,
    ProfileChangeView,
    ProfileDeleteView,
    TestedEmailView,
    TestedPasswordChangeView,
    TestedPasswordResetView,
    TestedPasswordSetView,
)

from .views import SelectLanguageTemplateView, search_results

sitemaps = {
    "flatpages": FlatPageSitemap,
}

urlpatterns = [
    path("admin/filebrowser/", site.urls),
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/login/", HTMXLoginView.as_view(), name="account_login"),
    path("accounts/logout/", HTMXLogoutView.as_view(), name="account_logout"),
    path("accounts/signup/", HTMXSignupView.as_view(), name="account_signup"),
    path("accounts/contact/", ContactFormView.as_view(), name="account_contact"),
    path("accounts/profile/", ProfileChangeView.as_view(), name="account_profile"),
    path(
        "accounts/profile/delete/", ProfileDeleteView.as_view(), name="account_delete"
    ),
    path(
        "accounts/password/change/",
        TestedPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password/set/", TestedPasswordSetView.as_view(), name="password_set"
    ),
    path(
        "accounts/password/reset/",
        TestedPasswordResetView.as_view(),
        name="password_reset",
    ),
    path("accounts/email/", TestedEmailView.as_view(), name="account_email"),
    path("accounts/", include("allauth.urls")),
    path("docs/", include("django.contrib.flatpages.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("build-api/", include("buildings.api_urls")),
]

urlpatterns += i18n_patterns(
    path("", HomePageTemplateView.as_view(), name="home"),
    path(_("search/"), search_results, name="search_results"),
    path(
        _("select-language/"),
        SelectLanguageTemplateView.as_view(),
        name="select_language",
    ),
    path(_("articles/"), include("pages.urls", namespace="pages")),
    path(_("buildings/"), include("buildings.urls", namespace="buildings")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
