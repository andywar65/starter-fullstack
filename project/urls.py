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
from django.urls import path, include # re_path,
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='home'),
    path('api-auth/', include('rest_framework.urls')),
    # this url is used to generate email content
    #re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        #TemplateView.as_view(template_name="password_reset_confirm.html"),
        #name='password_reset_confirm'),
    #path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    #path('api/v1/dj-rest-auth/registration/',
        #include('dj_rest_auth.registration.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/v1/users/', include('users.api.v1.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
