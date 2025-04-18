from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SignupSerializer, LoginSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from .schemas import (
    ErrorResponseSerializer,
    TokenResponseSerializer,
    MessageResponseSerializer,
    SIGNUP_REQUEST_EXAMPLE,
    SIGNUP_SUCCESS_EXAMPLE,
    SIGNUP_ERROR_EXAMPLE,
    LOGIN_REQUEST_EXAMPLE,
    LOGIN_SUCCESS_EXAMPLE,
    LOGIN_ERROR_EXAMPLE,
    AUTH_SUCCESS_EXAMPLE,
    TOKEN_EXPIRED_EXAMPLE,
    INVALID_TOKEN_EXAMPLE,
    TOKEN_NOT_FOUND_EXAMPLE,
)

"""
APIView 구현

schemas.py에서 API 문서화 관련 코드를 모듈화하여:
- 코드 중복을 제거하고 유지보수성을 높였습니다.
- 재사용 가능한 응답 형식과 예시를 활용하여 문서화 효율성을 증대했습니다.
- 모든 API 응답이 일관된 형식을 유지하도록 표준화했습니다.
"""

@extend_schema(
    tags=["Signup"],
    operation_id="2_signup",
    description="회원가입을 위한 API.",
    request=SignupSerializer,
    responses={201: SignupSerializer, 400: ErrorResponseSerializer},
    examples=[SIGNUP_REQUEST_EXAMPLE, SIGNUP_SUCCESS_EXAMPLE, SIGNUP_ERROR_EXAMPLE],
)
class SignupAPIView(APIView):
    # 모든 사용자가 접근 가능하도록 설정
    permission_classes = [AllowAny]

    # 회원가입 기능
    def post(self, request):
        # 요청 데이터를 직렬화
        serializer = SignupSerializer(data=request.data)

        # 직렬화된 데이터가 유효한 경우
        if serializer.is_valid():
            # 데이터를 DB에 저장
            try:
                user = serializer.save()
                return Response(
                    {"username": user.username, "nickname": user.nickname},
                    status=status.HTTP_201_CREATED,
                )
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Login"],
    operation_id="1_login",
    description="로그인을 위한 API.",
    request=LoginSerializer,
    responses={200: TokenResponseSerializer, 400: ErrorResponseSerializer},
    examples=[LOGIN_REQUEST_EXAMPLE, LOGIN_SUCCESS_EXAMPLE, LOGIN_ERROR_EXAMPLE],
)
class LoginAPIView(APIView):
    # 모든 사용자가 접근 가능하도록 설정
    permission_classes = [AllowAny]

    # 로그인 기능
    # 서버의 상태를 변경하는 기능이므로 POST 요청을 사용
    def post(self, request):
        # LoginSerializer를 사용하여 데이터 검증
        serializer = LoginSerializer(data=request.data)

        # 직렬화된 데이터가 유효한 경우
        if serializer.is_valid():
            # 검증된 데이터에서 user 객체 가져오기
            user = serializer.validated_data["user"]

            # 토큰 생성
            access_token = AccessToken.for_user(user)
            return Response({"token": str(access_token)}, status=status.HTTP_200_OK)
        else:
            # 직렬화 에러 반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
    tags=["Auth-Test"],
    operation_id="3_auth_test",
    description="인증 테스트를 위한 API.",
    responses={200: MessageResponseSerializer, 401: ErrorResponseSerializer},
    examples=[
        AUTH_SUCCESS_EXAMPLE,
        TOKEN_EXPIRED_EXAMPLE,
        INVALID_TOKEN_EXAMPLE,
        TOKEN_NOT_FOUND_EXAMPLE,
    ],
)
class AuthTestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 인증 테스트 기능
    def get(self, request):
        return Response({"message": "인증 성공"}, status=status.HTTP_200_OK)
