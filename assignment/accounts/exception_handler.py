from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # 예외 객체에 직접 커스텀 형식이 있는지 먼저 확인
    if hasattr(exc, 'detail') and isinstance(exc.detail, dict) and 'error' in exc.detail:
        # 예외 객체의 원본 데이터를 기반으로 응답 생성
        return Response(exc.detail, status=exc.status_code)
    
    # 기본 예외 처리를 호출
    response = exception_handler(exc, context)
    
    # 기본 핸들러가 처리하지 않은 경우 None 반환
    if response is None:
        return None
        
    # 인증 관련 예외 처리 (401 에러)
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        error_code = "AUTHENTICATION_ERROR"
        error_message = "인증에 실패했습니다."
        
        # AuthenticationFailed 예외 세부 처리
        if isinstance(exc, AuthenticationFailed):
            error_code = "AUTHENTICATION_FAILED"
            
            # 오류 메시지에 따라 다른 코드 반환
            error_str = str(exc.detail).lower()
            if "expired" in error_str:
                error_code = "TOKEN_EXPIRED"
                error_message = "토큰이 만료되었습니다."
            elif "invalid" in error_str:
                error_code = "INVALID_TOKEN"
                error_message = "토큰이 유효하지 않습니다."
            else:
                error_message = "잘못된 인증 정보입니다."
        
        # NotAuthenticated 예외 세부 처리
        elif isinstance(exc, NotAuthenticated):
            error_code = "TOKEN_NOT_FOUND"
            
            # 오류 메시지에 따라 다른 메시지 반환
            error_str = str(exc.detail).lower()
            if error_str or "no token" in error_str:
                error_message = "토큰이 없습니다."
            
        # 응답 데이터 구조화
        response.data = {
            "error": {
                "code": error_code,
                "message": error_message
            }
        }
        
    return response 