from django.urls import path

from .views import (
    ArticleArchiveIndexView,
    ArticleDayArchiveView,
    ArticleDetailView,
    ArticleMonthArchiveView,
    ArticleYearArchiveView,
    ShotgunArchiveIndexView,
)

app_name = "pages"
urlpatterns = [
    path("", ArticleArchiveIndexView.as_view(), name="article_index"),
    path("shotgun/", ShotgunArchiveIndexView.as_view(), name="shotgun_index"),
    path("<int:year>/", ArticleYearArchiveView.as_view(), name="article_year"),
    path(
        "<int:year>/<int:month>/",
        ArticleMonthArchiveView.as_view(),
        name="article_month",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/",
        ArticleDayArchiveView.as_view(),
        name="article_day",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
]
