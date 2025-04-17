from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
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

    # 검증
    def validate(self, data):
        
        # 중복 사용자 검증
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({
                "error": {
                    "code": "USER_ALREADY_EXISTS",
                    "message": "이미 가입된 사용자입니다."
                }
            })
        
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        
        # body에 아이디와 비밀번호가 있는지 검증
        username = data.get('username')
        password = data.get('password')
        
        # 사용자 인증
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError({
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "아이디 또는 비밀번호가 올바르지 않습니다."
                }
            })
            
        # 인증 성공한 사용자 정보 반환
        data['user'] = user
        return data