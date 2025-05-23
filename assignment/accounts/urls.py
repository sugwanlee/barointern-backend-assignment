from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("auth-test/", views.AuthTestAPIView.as_view(), name="auth-test"),
]
