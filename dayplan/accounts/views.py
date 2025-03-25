from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializer import RegisterSerializer,UserSerializer, PasswordSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
# Create your views here.

User = get_user_model()

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 调用发送验证邮件逻辑可以在这里执行
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data)

    def put(self, request):
        user = UserSerializer(request.user, data=request.data, partial=True)
        if user.is_valid():
            user.save()
            return Response(user.data)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not check_password(serializer.validated_data['old_password'], request.user.password):
                return Response({'error': '旧密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    """返回 CSRF 令牌的 API 端点"""
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

def logout_view(request):
    logout(request)  # 清除 Session
    return JsonResponse({"message": "退出成功"})
