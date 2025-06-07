from rest_framework import serializers
from users.models import User, Role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

# class PermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permission
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'phone', 'address', 'name']
#         read_only_fields = ['id']
#         extra_kwargs = {
#             'username': {'required': True},
#             'email': {'required': True},
#         }

#     def get_name(self, obj):
#         return obj.name
    
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'name']
        read_only_fields = ['id']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request:
            method = request.method

            if method in ['PUT', 'PATCH']:
                # On update, prevent sending username
                self.fields.pop('username')

    def to_representation(self, instance):
        """ Show 'name' as first + last """
        ret = super().to_representation(instance)
        ret['name'] = f"{instance.first_name} {instance.last_name}".strip()
        return ret

    def to_internal_value(self, data):
        """ When receiving 'name', split into first and last """
        internal = super().to_internal_value(data)
        name = data.get('name', '')
        parts = name.split()
        internal['first_name'] = parts[0] if len(parts) >= 1 else ''
        internal['last_name'] = ' '.join(parts[1:]) if len(parts) > 1 else ''
        return internal
    #gpt


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()