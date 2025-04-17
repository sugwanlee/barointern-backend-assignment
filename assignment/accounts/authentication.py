from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raise exceptions.AuthenticationFailed({
                "error": {
                    "code": "TOKEN_NOT_FOUND",
                    "message": "토큰이 없습니다."
                }
            })

        try:
            raw_token = self.get_raw_token(header)
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except TokenError as e:
            if 'expired' in str(e):
                raise exceptions.AuthenticationFailed({
                    "error": {
                        "code": "TOKEN_EXPIRED",
                        "message": "토큰이 만료되었습니다."
                    }
                })
            else:
                raise exceptions.AuthenticationFailed({
                    "error": {
                        "code": "INVALID_TOKEN",
                        "message": "토큰이 유효하지 않습니다."
                    }
                }) 