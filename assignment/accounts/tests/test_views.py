import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        nickname='testnick'
    )

@pytest.mark.django_db
def test_signup_success(client):
    url = reverse('signup')
    data = {
        'username': 'newuser',
        'password': 'newpass123',
        'nickname': 'newnick'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_signup_duplicate_username(client, test_user):
    url = reverse('signup')
    data = {
        'username': 'testuser',  # 이미 존재하는 username
        'password': 'newpass123',
        'nickname': 'newnick'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error']['code'] == 'USER_ALREADY_EXISTS'

@pytest.mark.django_db
def test_login_success(client, test_user):
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

@pytest.mark.django_db
def test_login_wrong_password(client, test_user):
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'wrongpass'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error']['code'] == 'INVALID_CREDENTIALS' 