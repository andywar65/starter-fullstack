from django.urls import path

from .views import (
    ShotgunArchiveLimited,
    ShotgunCreateFormView,
    ShotgunFeed,
    ShotgunStoryListView,
    StoryListView,
)

app_name = "pages"
urlpatterns = [
    path(
        "<int:pk>/<slug:slug>/",
        ShotgunArchiveLimited.as_view(),
        name="shotgun_detail",
    ),
    path(
        "<int:pk>/",
        ShotgunArchiveLimited.as_view(),
        name="shotgun_detail_unslug",
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
    path(
        "feed/",
        ShotgunFeed(),
        name="shotgun_feed",
    ),
    path(
        "stories/",
        StoryListView.as_view(),
        name="story_list",
    ),
    path(
        "stories/<int:pk>/<slug:slug>/",
        ShotgunStoryListView.as_view(),
        name="story_detail",
    ),
]
