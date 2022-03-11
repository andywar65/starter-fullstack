from django.urls import path, re_path

from allauth.account.views import (account_inactive, email_verification_sent,
    confirm_email, password_reset_done, password_reset_from_key,
    password_reset_from_key_done)

from .views import *

urlpatterns = [
    path('login/', HTMXLoginView.as_view(), name='account_login'),
    path('logout/', HTMXLogoutView.as_view(), name='account_logout'),
    path('signup/', HTMXSignupView.as_view(), name='account_signup'),
    path('profile/', ProfileChangeView.as_view(), name='account_profile'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='account_delete'),
    path('password/change/', TestedPasswordChangeView.as_view(), name='password_change'),
    path('password/set/', TestedPasswordSetView.as_view(), name='password_set'),
    path('password/reset/', TestedPasswordResetView.as_view(), name='password_reset'),
    path('email/', TestedEmailView.as_view(), name='account_email'),
    path("inactive/", account_inactive, name="account_inactive"),
    # E-mail
    path(
        "confirm-email/", email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$", confirm_email,
        name="account_confirm_email",
    ),
    # password reset
    path(
        "password/reset/done/", password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/", password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
]
