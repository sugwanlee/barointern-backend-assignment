"""
API 문서화를 위한 스키마 및 예시 정의 모듈

이 모듈은 다음과 같은 이유로 API 문서화 관련 코드를 별도로 모듈화했습니다:
1. 코드 유지보수성 향상: 
   - API 응답 형식이 변경되어도 한 곳에서만 수정하면 됩니다.
   - 문서화 로직과 비즈니스 로직을 분리하여 관심사 분리(Separation of Concerns) 원칙을 준수합니다.

2. 재사용성 확보:
   - 여러 API에서 동일한 응답 형식과 예시를 재사용할 수 있습니다.
   - 새로운 API 추가 시 기존에 정의된 스키마를 활용할 수 있습니다.

3. 일관성 유지:
   - 모든 API가 동일한 응답 형식과 스타일을 유지할 수 있습니다.
   - 표준화된 에러 응답 형식을 적용하여 클라이언트 개발자의 이해도를 높입니다.
"""

from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample

    
# 에러 응답 시리얼라이저
class ErrorDetailSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    error = ErrorDetailSerializer()
    
# 토큰 응답 시리얼라이저
class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()

# 메시지 응답 시리얼라이저
class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

# 공통 예시 정의
# 회원가입 예시
SIGNUP_REQUEST_EXAMPLE = OpenApiExample(
    '회원가입 요청',
    request_only=True,
    value={
        'username': 'JIN HO',
        'password': '12341234',
        'nickname': 'Mentos'
    }
)

SIGNUP_SUCCESS_EXAMPLE = OpenApiExample(
    '회원가입 성공 응답',
    response_only=True,
    status_codes=['201'],
    value={
        'username': 'JIN HO',
        'nickname': 'Mentos'
    }
)

SIGNUP_ERROR_EXAMPLE = OpenApiExample(
    '회원가입 실패 응답',
    response_only=True,
    status_codes=['400'],
    value={
        'error': {
            'code': 'USER_ALREADY_EXISTS',
            'message': '이미 가입된 사용자입니다.'
        }
    }
)

# 로그인 예시
LOGIN_REQUEST_EXAMPLE = OpenApiExample(
    '로그인 요청',
    request_only=True,
    value={
        'username': 'JIN HO',
        'password': '12341234'
    }
)

LOGIN_SUCCESS_EXAMPLE = OpenApiExample(
    '로그인 성공 응답',
    response_only=True,
    status_codes=['200'],
    value={
        'token': 'eKDIkdfjoakIdkfjpekdkcjdkoIOdjOKJDFOlLDKFJKL'
    }
)

LOGIN_ERROR_EXAMPLE = OpenApiExample(
    '로그인 실패 응답',
    response_only=True,
    status_codes=['400'],
    value={
        'error': {
            'code': 'INVALID_CREDENTIALS',
            'message': '아이디 또는 비밀번호가 올바르지 않습니다.'
        }
    }
)

# 인증 관련 예시
AUTH_SUCCESS_EXAMPLE = OpenApiExample(
    '인증 성공 응답',
    response_only=True,
    status_codes=['200'],
    value={
        'message': '인증 성공'
    }
)

TOKEN_EXPIRED_EXAMPLE = OpenApiExample(
    '만료된 토큰',
    response_only=True,
    status_codes=['401'],
    value={
        'error': {
            'code': 'TOKEN_EXPIRED',
            'message': '토큰이 만료되었습니다.'
        }
    }
)

INVALID_TOKEN_EXAMPLE = OpenApiExample(
    '유효하지 않은 토큰',
    response_only=True,
    status_codes=['401'],
    value={
        'error': {
            'code': 'INVALID_TOKEN',
            'message': '토큰이 유효하지 않습니다.'
        }
    }
)

TOKEN_NOT_FOUND_EXAMPLE = OpenApiExample(
    '토큰 없음',
    response_only=True,
    status_codes=['401'],
    value={
        'error': {
            'code': 'TOKEN_NOT_FOUND',
            'message': '토큰이 없습니다.'
        }
    }
) 