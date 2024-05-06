"""djpress URLs file."""

from django.conf import settings
from django.urls import path, re_path

from djpress.feeds import PostFeed
from djpress.views import (
    author_posts,
    category_posts,
    date_archives,
    index,
    post_detail,
)

regex_path = r"^(?P<path>[0-9A-Za-z_.//-]*)/$"
regex_year = r"^(?P<year>\d{4})/$"
regex_month = r"^(?P<year>\d{4})/(?P<month>\d{2})/$"
regex_day = r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$"

app_name = "djpress"

urlpatterns = []

if settings.CATEGORY_PATH:
    urlpatterns += [
        path(
            f"{settings.CATEGORY_PATH}/<slug:slug>/",
            category_posts,
            name="category_posts",
        ),
    ]

if settings.AUTHOR_PATH:
    urlpatterns += [
        path(
            f"{settings.AUTHOR_PATH}/<str:author>/",
            author_posts,
            name="author_posts",
        ),
    ]

if settings.RSS_PATH:
    urlpatterns += [
        path(f"{settings.RSS_PATH}/", PostFeed(), name="rss_feed"),
    ]

if settings.DATE_ARCHIVES:
    urlpatterns += [
        re_path(
            regex_day,
            date_archives,
            name="day_archive",
        ),
        re_path(
            regex_month,
            date_archives,
            name="month_archive",
        ),
        re_path(
            regex_year,
            date_archives,
            name="year_archive",
        ),
    ]

urlpatterns += [
    path("", index, name="index"),
    re_path(regex_path, post_detail, name="post_detail"),
]
