from django.urls import path

from .views import (
    ShotgunArchiveLimited,
    ShotgunCreateFormView,
    ShotgunFeed,
    ShotgunStoryListView,
    StoryListView,
    StorySelectFormView,
)

app_name = "pages"
urlpatterns = [
    path(
        "<int:pk>/<slug:slug>/",
        ShotgunArchiveLimited.as_view(),
        name="shotgun_detail",
    ),
    # legacy URLs without slugs
    path(
        "<int:pk>/",
        ShotgunArchiveLimited.as_view(),
        name="shotgun_detail_unslug",
    ),
    # legacy URLs with old "shot" prefix
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
    # never used, use action_with_form instead
    path(
        "associate/",
        StorySelectFormView.as_view(),
        name="shotgun_associate",
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
