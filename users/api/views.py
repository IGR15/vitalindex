from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsDoctor,IsNurse,IsStudent
from users.models import User,Role,Permission,UserRolePermission
from users.utiles import check_user_permission_level
from django.shortcuts import get_object_or_404
from users.api.serializers import (UserSerializer,
                                   PermissionSerializer,
                                   RoleSerializer)


class AssignPermissionToRole(APIView):
    permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        role_id = request.data.get('role_id')
        permission_id = request.data.get('permission_id')

        if not role_id or not permission_id:
            return Response({"error": "role_id and permission_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        role = get_object_or_404(Role, pk=role_id)
        permission = get_object_or_404(Permission, pk=permission_id)

        if UserRolePermission.objects.filter(role=role, permission=permission).exists():
            return Response({"message": "Permission already assigned to this role"}, status=status.HTTP_200_OK)

        UserRolePermission.objects.create(role=role, permission=permission)
        return Response({"message": f"Permission '{permission.name}' assigned to role '{role.name}'"}, status=status.HTTP_201_CREATED)

class UserList(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser] 
    def get(self,request):
        try:
            user=User.objects.all()
        except User.DoesNotExist:
            return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
class UserDetail(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser] 

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)    
    def put(self,request,pk):
        try:
            user=User.objects.get(pk=pk)
            serializer = UserSerializer(user,data=request.data)
        except User.DoesNotExist:
            return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)    
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self,request,pk):
        try:
            user=User.objects.get(pk=pk)
            user.delete()
        except User.DoesNotExist:
            return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)    
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserByRole(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser,IsDoctor,IsNurse] 

    def get(self, request, role_id):
        users = User.objects.filter(role__id=role_id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)   
    
class SingleUserByRole(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser,IsDoctor,IsNurse] 

    def get(self, request, role_id, user_id):
        try:
            user = User.objects.get(role__id=role_id, id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found in this role'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)     


class UserCreate(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser]
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    


    
class  permissionsList(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser]
    def get(self,request):   
        try:
            
            permissions = Permission.objects.all()
        except Permission.DoesNot:
            return Response({'error':'permissions not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    
class PermissionsList(APIView):   
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser] 
    def get(self,request):
        try:
            permissions = Permission.objects.all()
        except Permission.DoesNotExist:
            return Response({'error':'permissions not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

class CreatePermission(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser]
    def post(self,request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class Permissions(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            permission = Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            return Response({'error':'permission not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            permission=Permission.objects.get(pk=pk)
            serializer = PermissionSerializer(permission,data=request.data)
        except Permission.DoesNotExist:
            return Response({'error':'permission not found'},status=status.HTTP_404_NOT_FOUND)    
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            permission=Permission.objects.get(pk=pk)
            permission.delete()
        except Permission.DoesNotExist:
            return Response({'error':'permission not found'},status=status.HTTP_404_NOT_FOUND)    
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class RoleList(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser]
    def get(self,request):
        try:
            roles = Role.objects.all()
        except Role.DoesNotExist:
            return Response({'error':'roles not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    
class CreateRole(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser]
    def post(self,request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


class RoleDetail(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return Response(serializer.data)
    def put(self, request, pk):
        try:
            role=Role.objects.get(pk=pk)
            serializer = RoleSerializer(role,data=request.data)
        except Role.DoesNotExist:
            return Response({'error':'role not found'},status=status.HTTP_404_NOT_FOUND)    
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk):
        try:
            role=Role.objects.get(pk=pk)
            role.delete()
        except Role.DoesNotExist:
            return Response({'error':'role not found'},status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    