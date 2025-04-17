from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    # 비밀번호 필드를 쓰기 전용으로 설정
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    # 모델과 필드 설정
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname')
        extra_kwargs = {
            'username': {
                'required': True,
                'validators': []  # 기본 validators 비활성화
            },
            'nickname': {'required': True}
        }

    # 데이터 저장 기능
    def create(self, validated_data):
        # 데이터 저장
        user = User.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname']
        )
        # 비밀번호 설정
        user.set_password(validated_data['password'])
        # 데이터 저장
        user.save()
        return user

    # 필수 필드 검증
    def validate(self, data):
        # 필수 필드 검증
        if not data.get('username') or not data.get('password') or not data.get('nickname'):
            raise serializers.ValidationError({
                "error": {
                    "code": "MISSING_CREDENTIALS",
                    "message": "아이디, 비밀번호, 닉네임을 모두 입력해주세요."
                }
            })
        
        # 중복 사용자 검증
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({
                "error": {
                    "code": "USER_ALREADY_EXISTS",
                    "message": "이미 가입된 사용자입니다."
                }
            })
        
        return data