import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_returns_jwt(api_client):
    response = api_client.post(
        "/api/v1/auth/register/",
        {"username": "ada", "email": "ada@example.com", "password": "Str0ngPass!234"},
        format="json",
    )
    assert response.status_code == 201
    assert "access" in response.data["tokens"]
