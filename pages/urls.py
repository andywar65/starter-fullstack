from django.urls import path

from .views import ShotgunArchiveLimited, ShotgunCreateFormView

app_name = "pages"
urlpatterns = [
    path(
        "<int:pk>/",
        ShotgunArchiveLimited.as_view(),
        name="shotgun_detail",
    ),
    path(
        "shot/<int:pk>/",
        ShotgunArchiveLimited.as_view(),
        name="shotgun_detail_legacy",
    ),
    path(
        "add/",
        ShotgunCreateFormView.as_view(),
        name="shotgun_create",
    ),
]
