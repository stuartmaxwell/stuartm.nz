import pytest

from django.contrib.auth.models import User

from djpress.models import Category, Post


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def category1():
    return Category.objects.create(title="Test Category1", slug="test-category1")


@pytest.fixture
def category2():
    return Category.objects.create(title="Test Category2", slug="test-category2")


@pytest.fixture
def category3():
    category = Category.objects.create(title="Development", slug="dev")
    return category


@pytest.fixture
def test_post1(user, category1):
    post = Post.objects.create(
        title="Test Post1",
        slug="test-post1",
        content="This is test post 1.",
        author=user,
        status="published",
        post_type="post",
    )
    post.categories.set([category1])

    return post


@pytest.fixture
def test_post2(user, category2):
    post = Post.objects.create(
        title="Test Post2",
        slug="test-post2",
        content="This is test post 2.",
        author=user,
        status="published",
        post_type="post",
    )
    post.categories.set([category2])
    return post


@pytest.fixture
def test_post3(user, category1):
    post = Post.objects.create(
        title="Test Post3",
        slug="test-post3",
        content="This is test post 3.",
        author=user,
        status="published",
        post_type="post",
    )

    return post


@pytest.fixture
def test_long_post1(user, settings, category1):
    truncate_tag = settings.DJPRESS_SETTINGS["TRUNCATE_TAG"]
    post = Post.post_objects.create(
        title="Test Long Post1",
        slug="test-long-post1",
        content=f"This is the truncated content.\n\n{truncate_tag}\n\nThis is the rest of the post.",
        author=user,
        status="published",
        post_type="post",
    )
    post.categories.set([category1])
    return post


@pytest.fixture
def test_page1(user):
    return Post.objects.create(
        title="Test Page1",
        slug="test-page1",
        content="This is test page 1.",
        author=user,
        status="published",
        post_type="page",
    )


@pytest.fixture
def test_page2(user):
    return Post.objects.create(
        title="Test Page2",
        slug="test-page2",
        content="This is test page 2.",
        author=user,
        status="published",
        post_type="page",
    )


@pytest.fixture
def test_page3(user):
    return Post.objects.create(
        title="Test Page3",
        slug="test-page3",
        content="This is test page 3.",
        author=user,
        status="published",
        post_type="page",
    )


@pytest.fixture
def test_page4(user):
    return Post.objects.create(
        title="Test Page4",
        slug="test-page4",
        content="This is test page 4.",
        author=user,
        status="published",
        post_type="page",
    )


@pytest.fixture
def test_page5(user):
    return Post.objects.create(
        title="Test Page5",
        slug="test-page5",
        content="This is test page 5.",
        author=user,
        status="published",
        post_type="page",
    )
