import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
import jwt
from django.conf import settings


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser", password="testpass123", nickname="testnick"
    )


@pytest.mark.django_db
def test_signup_success(client):
    url = reverse("signup")
    data = {"username": "newuser", "password": "newpass123", "nickname": "newnick"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"
    assert response.data["nickname"] == "newnick"
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_signup_duplicate_username(client, test_user):
    url = reverse("signup")
    data = {
        "username": "testuser",  # 이미 존재하는 username
        "password": "newpass123",
        "nickname": "newnick",
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "USER_ALREADY_EXISTS"
    assert response.data["error"]["message"] == "이미 가입된 사용자입니다."


@pytest.mark.django_db
def test_login_success(client, test_user):
    url = reverse("login")
    data = {"username": "testuser", "password": "testpass123"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


@pytest.mark.django_db
def test_login_wrong_password(client, test_user):
    url = reverse("login")
    data = {"username": "testuser", "password": "wrongpass"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"]["code"] == "INVALID_CREDENTIALS"
    assert (
        response.data["error"]["message"] == "아이디 또는 비밀번호가 올바르지 않습니다."
    )


@pytest.mark.django_db
def test_auth_no_token(client):
    url = reverse("auth-test")  # 보호된 엔드포인트
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "TOKEN_NOT_FOUND"
    assert response.data["error"]["message"] == "토큰이 없습니다."


@pytest.mark.django_db
def test_auth_invalid_token(client):
    url = reverse("auth-test")
    # credentials 대신 HTTP_AUTHORIZATION 헤더를 직접 전달
    response = client.get(url, HTTP_AUTHORIZATION="Bearer invalidtoken")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "INVALID_TOKEN"
    assert response.data["error"]["message"] == "토큰이 유효하지 않습니다."


@pytest.mark.django_db
def test_auth_expired_token(client, test_user, settings):
    # 토큰 생성
    token = AccessToken.for_user(test_user)

    # 토큰의 만료 시간을 과거로 직접 설정
    token_payload = jwt.decode(str(token), options={"verify_signature": False})

    # 토큰 만료 시간을 현재보다 10초 이전으로 설정 (시간대 인식 방식 사용)
    token_payload["exp"] = timezone.now().timestamp() - 10

    # 새로운 만료된 토큰 생성
    expired_token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm="HS256")

    url = reverse("auth-test")
    # 만료된 토큰으로 요청
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {expired_token}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["error"]["code"] == "TOKEN_EXPIRED"
    assert response.data["error"]["message"] == "토큰이 만료되었습니다."
