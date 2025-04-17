from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer

# Create your views here.

# 회원가입 기능
class SignupAPIView(APIView):
    # 모든 사용자가 접근 가능하도록 설정
    permission_classes = [AllowAny]

    # 회원가입 기능
    # DB에 저장하는 기능이므로 POST 요청을 사용
    def post(self, request):
        # 요청 데이터를 직렬화
        serializer = SignupSerializer(data=request.data)

        # 직렬화된 데이터가 유효한 경우
        if serializer.is_valid(raise_exception=True):
            # 데이터를 DB에 저장
            user = serializer.save()
            return Response({
                'username': user.username,
                'nickname': user.nickname
            }, status=status.HTTP_201_CREATED)

# 로그인 기능
class LoginAPIView(APIView):
    # 모든 사용자가 접근 가능하도록 설정
    permission_classes = [AllowAny]

    # 로그인 기능
    # 서버의 상태를 변경하는 기능이므로 POST 요청을 사용
    def post(self, request):
        # 요청 데이터에서 아이디와 비밀번호를 가져옴
        username = request.data.get('username')
        password = request.data.get('password')

        # 아이디와 비밀번호가 모두 입력되지 않은 경우
        if not username or not password:
            return Response(
                {"error": {"code": "MISSING_CREDENTIALS", "message": "아이디와 비밀번호를 모두 입력해주세요."}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 아이디와 비밀번호가 일치하는 경우 사용자 객체 반환
        user = authenticate(request, username=username, password=password)

        # 사용자 객체가 존재하는 경우
        if user is not None:
            # 토큰 생성
            access_token = AccessToken.for_user(user)
            return Response(
                {'token': str(access_token)},
                status=status.HTTP_200_OK
            )

        # 사용자 객체가 존재하지 않는 경우
        else:
            return Response(
                {"error": {"code": "INVALID_CREDENTIALS", "message": "아이디 또는 비밀번호가 올바르지 않습니다."}},
                status=status.HTTP_401_UNAUTHORIZED
            )