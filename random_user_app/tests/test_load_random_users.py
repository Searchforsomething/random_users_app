from unittest.mock import patch, MagicMock

import pytest
from django.core.management import call_command

from users.models import User


@pytest.mark.django_db
@patch("users.management.commands.load_random_users.requests.get")
def test_load_random_users_creates_users(mock_get):
    fake_users = [{
        "gender": "male",
        "name": {"first": "John", "last": "Doe"},
        "email": f"john{i}@example.com",
        "phone": f"123-456-7890{i}",
        "location": {"city": "City", "country": "Country"},
        "picture": {"thumbnail": "http://example.com/thumb.jpg"},
    } for i in range(100)]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": fake_users}
    mock_get.return_value = mock_response

    call_command("load_random_users", count=10)

    assert User.objects.count() == 10
    user = User.objects.first()
    assert user.email == "john0@example.com"
    assert user.first_name == "John"
    assert user.location == "City, Country"


@pytest.mark.django_db
@patch("users.management.commands.load_random_users.requests.get")
def test_load_skips_if_users_exist(mock_get):
    fake_users = [{
        "gender": "male",
        "name": {"first": "John", "last": "Doe"},
        "email": f"john{i // 2}@example.com",
        "phone": f"123-456-7890{i // 2}",
        "location": {"city": "City", "country": "Country"},
        "picture": {"thumbnail": "http://example.com/thumb.jpg"},
    } for i in range(100)]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": fake_users}
    mock_get.return_value = mock_response

    call_command("load_random_users", count=10)

    assert User.objects.count() == 10
    user = User.objects.last()
    assert user.email == "john9@example.com"


@pytest.mark.django_db
@patch("users.management.commands.load_random_users.requests.get")
def test_load_aborts_on_bad_response(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    call_command("load_random_users")

    assert User.objects.count() == 0
