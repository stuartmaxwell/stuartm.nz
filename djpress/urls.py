"""djpress URLs file."""

from django.urls import path

from djpress.feeds import ContentFeed
from djpress.views import category_posts, content_detail, index

app_name = "djpress"
urlpatterns = [
    path("", index, name="index"),
    path("post/<slug:slug>/", content_detail, name="content_detail"),
    path("category/<slug:slug>/", category_posts, name="category_posts"),
    path("rss/", ContentFeed(), name="rss_feed"),
]
