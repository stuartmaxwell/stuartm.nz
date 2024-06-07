from django.http import HttpResponse
from django.test import Client
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index(client: Client) -> None:
    """Test index view."""
    url = "/"
    response: HttpResponse = client.get(url)
    assert response.status_code == 200
