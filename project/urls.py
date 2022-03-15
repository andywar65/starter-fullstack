"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from filebrowser.sites import site

from .views import search_results, SelectLanguageTemplateView
from pages.views import HomePageTemplateView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    #path('accounts/', include('allauth.urls')),
    path('accounts/', include('users.urls')),
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
