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
from django.urls import path, include

from .views import *
from users.views import *

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', HTMXLoginView.as_view(), name='account_login'),
    path('accounts/logout/', HTMXLogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', HTMXSignupView.as_view(), name='account_signup'),
    path('accounts/profile/', ProfileChangeView.as_view(), name='account_profile'),
    path('accounts/profile/delete/', ProfileDeleteView.as_view(), name='account_delete'),
    path('accounts/password/change/', TestedPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password/set/', TestedPasswordSetView.as_view(), name='password_set'),
    path('accounts/password/reset/', TestedPasswordResetView.as_view(), name='password_reset'),
    path('accounts/email/', TestedEmailView.as_view(), name='account_email'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
