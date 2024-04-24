import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from djpress.models import Category, Content


@pytest.mark.django_db
def test_home_view(client):
    url = reverse("djpress:home")
    response = client.get(url)
    assert response.status_code == 200
    assert "posts" in response.context


@pytest.mark.django_db
def test_post_detail_view(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    content = Content.objects.create(
        title="Test Post",
        slug="test-post",
        content="This is a test post.",
        author=user,
        status="published",
        content_type="post",
    )
    url = reverse("djpress:post_detail", args=[content.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert "post" in response.context


@pytest.mark.django_db
def test_category_posts_view(client):
    category = Category.objects.create(name="Test Category", slug="test-category")
    url = reverse("djpress:category_posts", args=[category.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert "category" in response.context
    assert "posts" in response.context
