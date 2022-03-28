import debug_toolbar

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from filebrowser.sites import site

from .views import search_results, SelectLanguageTemplateView
from pages.views import HomePageTemplateView
from users.views import *

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/login/', HTMXLoginView.as_view(), name='account_login'),
    path('accounts/logout/', HTMXLogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', HTMXSignupView.as_view(), name='account_signup'),
    path('accounts/contact/', ContactFormView.as_view(),
        name='account_contact'),
    path('accounts/profile/', ProfileChangeView.as_view(),
        name='account_profile'),
    path('accounts/profile/delete/', ProfileDeleteView.as_view(),
        name='account_delete'),
    path('accounts/password/change/', TestedPasswordChangeView.as_view(),
        name='password_change'),
    path('accounts/password/set/', TestedPasswordSetView.as_view(),
        name='password_set'),
    path('accounts/password/reset/', TestedPasswordResetView.as_view(),
        name='password_reset'),
    path('accounts/email/', TestedEmailView.as_view(), name='account_email'),
    path('accounts/', include('allauth.urls')),
    path('docs/', include('django.contrib.flatpages.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += i18n_patterns(
    path('', HomePageTemplateView.as_view(), name='home'),
    path(_('search/'), search_results, name='search_results'),
    path(_('select-language/'), SelectLanguageTemplateView.as_view(),
        name='select_language'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
