import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_users():
    return [
        User.objects.create(
            gender='male',
            first_name=f'John{i}',
            last_name='Doe',
            phone=f'12345678{i}',
            email=f'user{i}@example.com',
            location='City, Country',
            thumbnail='http://example.com/image.jpg'
        )
        for i in range(5)
    ]


@pytest.mark.django_db
def test_user_list_view(api_client, create_users):
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] == 5
    assert 'id' in response.data['results'][0]


@pytest.mark.django_db
def test_user_detail_view(api_client, create_users):
    user = create_users[0]
    url = reverse('user-detail', kwargs={'id': user.id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['email'] == user.email


@pytest.mark.django_db
def test_random_user_view(api_client, create_users):
    url = reverse('random-user')
    response = api_client.get(url)
    assert response.status_code == 200
    assert 'email' in response.data


@pytest.mark.django_db
def test_random_user_view_empty(api_client):
    url = reverse('random-user')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['detail'] == 'No users in database.'
