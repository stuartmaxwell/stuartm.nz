import pytest

from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from django.utils import timezone


@pytest.mark.django_db
def test_index(client, test_post1) -> None:
    """Test index view."""
    url = "/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_archives(client, test_post1) -> None:
    """Test archives views."""
    test_post1.date = timezone.make_aware(timezone.datetime(2024, 6, 1))
    test_post1.save()

    url = "/2024/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200
    assert "Test Post1" in str(response.content)

    url = "/2024/06/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200
    assert "Test Post1" in str(response.content)


@pytest.mark.django_db
def test_single_post(client, test_post1) -> None:
    """Test single post view."""
    test_post1.date = timezone.make_aware(timezone.datetime(2024, 6, 1))
    test_post1.save()

    url = "/2024/06/test-post1/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200
    assert "Test Post1" in str(response.content)


@pytest.mark.django_db
def test_author_view(client, test_post1):
    """Test author view."""
    url = "/author/testuser/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200
    assert "Test Post1" in str(response.content)


@pytest.mark.django_db
def test_categories_vew(client, test_post1):
    """Test categories view."""
    url = "/category/test-category1/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200
    assert "Test Post1" in str(response.content)


@pytest.mark.django_db
def test_single_page(client, test_page1):
    """Test single page view."""
    url = "/test-page1/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200
    assert "Test Page1" in str(response.content)
