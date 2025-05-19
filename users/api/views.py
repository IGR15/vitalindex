import secrets
import string
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsDoctor,IsNurse,IsStudent
from users.models import User,Role
from users.utiles import check_user_permission_level
from django.shortcuts import get_object_or_404
from users.api.serializers import (UserSerializer,
                                   RoleSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role.name if user.role else None
        token['email'] = user.email
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# --- User Views ---

@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Users']))
class UserList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    @swagger_auto_schema(tags=['Users'])
    def get(self, request):
        try:
            user = User.objects.all()
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Users']))
@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Users']))
@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Users']))
class UserDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    @swagger_auto_schema(tags=['Users'])
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    @swagger_auto_schema(serializer=UserSerializer, tags=['Users'])
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Users']))
class UserByRole(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor, IsNurse]
    def get(self, request, role_id):
        users = User.objects.filter(role__id=role_id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Users']))
class SingleUserByRole(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor, IsNurse]

   
    def get(self, request, role_id, user_id):
        try:
            user = User.objects.get(role__id=role_id, id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found in this role'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    @swagger_auto_schema(
        request_body=UserSerializer,
        tags=["Users"]
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user = serializer.save()
            user.set_password(password)
            user.save()
            send_mail(
                subject="Your VitalIndex Login Credentials",
                message=f"Username: {user.username}\nPassword: {password}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Role Views ---

@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Roles']))
class RoleList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        try:
            roles = Role.objects.all()
        except Role.DoesNotExist:
            return Response({'error': 'roles not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Roles']))
@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Roles']))
@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Roles']))
class RoleDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=RoleSerializer, tags=['Roles'])
    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            serializer = RoleSerializer(role, data=request.data)
        except Role.DoesNotExist:
            return Response({'error': 'role not found'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            role.delete()
        except Role.DoesNotExist:
            return Response({'error': 'role not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
