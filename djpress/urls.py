"""djpress URLs file."""

from django.urls import path

from .feeds import ContentFeed
from .views import category_posts, home, post_detail

app_name = "djpress"
urlpatterns = [
    path("", home, name="home"),
    path("post/<slug:slug>/", post_detail, name="post_detail"),
    path("category/<slug:slug>/", category_posts, name="category_posts"),
    path("rss/", ContentFeed(), name="rss_feed"),
]
