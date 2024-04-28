import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from djpress.models import Content
from djpress.feeds import ContentFeed


@pytest.mark.django_db
def test_latest_posts_feed(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    Content.objects.create(
        title="Post 1", content="Content of post 1.", author=user, status="published"
    )
    Content.objects.create(
        title="Post 2", content="Content of post 2.", author=user, status="published"
    )

    url = reverse("djpress:rss_feed")
    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/rss+xml; charset=utf-8"

    feed = response.content.decode("utf-8")
    assert "<title>stuartm.nz</title>" in feed
    assert "<link>http://testserver/rss</link>" in feed
    assert "<description>stuartm.nz updates</description>" in feed
    assert "<item>" in feed
    assert "<title>Post 1</title>" in feed
    assert "<description>&lt;p&gt;Content of post 1.&lt;/p&gt;</description>" in feed
    assert "<title>Post 2</title>" in feed
    assert "<description>&lt;p&gt;Content of post 2.&lt;/p&gt;</description>" in feed


@pytest.mark.django_db
def test_truncated_posts_feed(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    Content.objects.create(
        title="Post 1",
        content="Content of post 1.<!--more-->Truncated content",
        author=user,
        status="published",
    )

    url = reverse("djpress:rss_feed")
    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/rss+xml; charset=utf-8"

    feed = response.content.decode("utf-8")
    assert "<title>stuartm.nz</title>" in feed
    assert "<link>http://testserver/rss</link>" in feed
    assert "<description>stuartm.nz updates</description>" in feed
    assert "<item>" in feed
    assert "<title>Post 1</title>" in feed
    assert "Truncated content" not in feed
    assert '&lt;a href="/post/post-1/"&gt;Read more&lt;/a&gt;&lt;/p&gt;' in feed
