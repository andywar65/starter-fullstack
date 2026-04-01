from django.urls import path

from .views import ShotgunArchiveLimited, ShotgunCreateFormView

app_name = "pages"
urlpatterns = [
    # path("shotgun/", ShotgunArchiveIndexView.as_view(), name="shotgun_index"),
    path(
        "shot/<int:pk>/",
        ShotgunArchiveLimited.as_view(),
        name="shotgun_detail",
    ),
    path(
        "shot/add/",
        ShotgunCreateFormView.as_view(),
        name="shotgun_create",
    ),
]
