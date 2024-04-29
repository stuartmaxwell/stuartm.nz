import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from djpress.models import Category, Content


@pytest.mark.django_db
def test_index_view(client):
    url = reverse("djpress:index")
    response = client.get(url)
    print(response.content)
    assert response.status_code == 200
    assert b"No posts available" in response.content


@pytest.mark.django_db
def test_content_detail_view(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    content = Content.post_objects.create(
        title="Test Post",
        slug="test-post",
        content="This is a test post.",
        author=user,
        status="published",
        content_type="post",
    )
    url = reverse("djpress:content_detail", args=[content.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert "post" in response.context


@pytest.mark.django_db
def test_content_detail_not_exist(client):
    url = reverse("djpress:content_detail", args=["foobar-does-not-exist"])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_category_posts_view(client):
    category = Category.objects.create(name="Test Category", slug="test-category")
    url = reverse("djpress:category_posts", args=[category.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert "category" in response.context
    assert "posts" in response.context
