from rest_framework import serializers
from users.models import User, Role, Permission

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'address']