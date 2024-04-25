import pytest
from django.contrib.auth.models import User
from djpress.models import Category, Content
from django.utils import timezone


@pytest.mark.django_db
def test_category_model():
    category = Category.objects.create(name="Test Category", slug="test-category")
    assert category.name == "Test Category"
    assert category.slug == "test-category"
    assert str(category) == "Test Category"


@pytest.mark.django_db
def test_content_model():
    user = User.objects.create_user(username="testuser", password="testpass")
    category = Category.objects.create(name="Test Category", slug="test-category")
    content = Content.objects.create(
        title="Test Content",
        slug="test-content",
        content="This is a test content.",
        author=user,
        status="published",
        content_type="post",
    )
    content.categories.add(category)
    assert content.title == "Test Content"
    assert content.slug == "test-content"
    assert content.author == user
    assert content.status == "published"
    assert content.content_type == "post"
    assert content.categories.count() == 1
    assert str(content) == "Test Content"


@pytest.mark.django_db
def test_content_methods():
    user = User.objects.create_user(username="testuser", password="testpass")
    category = Category.objects.create(name="Test Category", slug="test-category")
    Content.objects.create(
        title="Test Post 1",
        slug="test-post-1",
        content="This is test post 1.",
        author=user,
        status="published",
        content_type="post",
    )
    Content.objects.create(
        title="Test Post 2",
        slug="test-post-2",
        content="This is test post 2.",
        author=user,
        status="draft",
        content_type="post",
    )
    Content.objects.create(
        title="Test Page",
        slug="test-page",
        content="This is a test page.",
        author=user,
        status="published",
        content_type="page",
    )
    assert Content.get_published_posts().count() == 1
    assert Content.get_published_post_by_slug("test-post-1").title == "Test Post 1"
    assert Content.get_published_posts_by_category(category).count() == 0


@pytest.mark.django_db
def test_get_published_posts_with_future_date():
    user = User.objects.create_user(username="testuser", password="testpass")
    Content.objects.create(
        title="Past Post",
        slug="past-post",
        content="This is a past post.",
        author=user,
        status="published",
        content_type="post",
        date=timezone.now() - timezone.timedelta(days=1),
    )
    Content.objects.create(
        title="Future Post",
        slug="future-post",
        content="This is a future post.",
        author=user,
        status="published",
        content_type="post",
        date=timezone.now() + timezone.timedelta(days=1),
    )
    assert Content.get_published_posts().count() == 1


@pytest.mark.django_db
def test_get_published_posts_ordering():
    user = User.objects.create_user(username="testuser", password="testpass")
    Content.objects.create(
        title="Older Post",
        slug="older-post",
        content="This is an older post.",
        author=user,
        status="published",
        content_type="post",
        date=timezone.now() - timezone.timedelta(days=2),
    )
    Content.objects.create(
        title="Newer Post",
        slug="newer-post",
        content="This is a newer post.",
        author=user,
        status="published",
        content_type="post",
        date=timezone.now() - timezone.timedelta(days=1),
    )
    posts = Content.get_published_posts()
    assert posts[0].title == "Newer Post"
    assert posts[1].title == "Older Post"


@pytest.mark.django_db
def test_get_published_post_by_slug_with_future_date():
    user = User.objects.create_user(username="testuser", password="testpass")
    Content.objects.create(
        title="Future Post",
        slug="future-post",
        content="This is a future post.",
        author=user,
        status="published",
        content_type="post",
        date=timezone.now() + timezone.timedelta(days=1),
    )
    with pytest.raises(Content.DoesNotExist):
        Content.get_published_post_by_slug("future-post")


@pytest.mark.django_db
def test_get_published_posts_by_category_with_future_date():
    user = User.objects.create_user(username="testuser", password="testpass")
    category = Category.objects.create(name="Test Category", slug="test-category")
    Content.objects.create(
        title="Past Post",
        slug="past-post",
        content="This is a past post.",
        author=user,
        status="published",
        content_type="post",
        date=timezone.now() - timezone.timedelta(days=1),
    ).categories.add(category)
    Content.objects.create(
        title="Future Post",
        slug="future-post",
        content="This is a future post.",
        author=user,
        status="published",
        content_type="post",
        date=timezone.now() + timezone.timedelta(days=1),
    ).categories.add(category)
    assert Content.get_published_posts_by_category(category).count() == 1
