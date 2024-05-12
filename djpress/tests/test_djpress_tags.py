import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from djpress.models import Post
from django.conf import settings

from djpress.templatetags import djpress_tags


@pytest.fixture
def user():
    user = User.objects.create_user(
        username="testuser",
        password="testpass",
        first_name="Test",
        last_name="User",
    )
    return user


@pytest.fixture
def create_test_post(user):
    post = Post.post_objects.create(
        title="Test Post",
        slug="test-post",
        content="This is a test post.",
        author=user,
        status="published",
        post_type="post",
    )
    return post


def test_get_blog_title():
    assert djpress_tags.get_blog_title() == settings.BLOG_TITLE


@pytest.mark.django_db
def test_post_author_link_without_author_path(create_test_post):
    settings.AUTHOR_PATH_ENABLED = False
    assert (
        djpress_tags.post_author_link(create_test_post)
        == create_test_post.author_display_name
    )


@pytest.mark.django_db
def test_post_author_link_with_author_path(create_test_post):
    settings.AUTHOR_PATH_ENABLED = True
    author_url = reverse("djpress:author_posts", args=[create_test_post.author])
    expected_output = (
        f'<a href="{author_url}" title="View all posts by '
        f'{ create_test_post.author_display_name }">{ create_test_post.author_display_name }</a>'
    )
    assert djpress_tags.post_author_link(create_test_post) == expected_output
