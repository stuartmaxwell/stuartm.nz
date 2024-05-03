"""djpress URLs file."""

from django.urls import path

from djpress.feeds import PostFeed
from djpress.views import category_posts, index, post_detail

app_name = "djpress"
urlpatterns = [
    path("", index, name="index"),
    path("post/<slug:slug>/", post_detail, name="post_detail"),
    path("category/<slug:slug>/", category_posts, name="category_posts"),
    path("rss/", PostFeed(), name="rss_feed"),
]
