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
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'name', 'gender']
        read_only_fields = ['id']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method in ['PUT', 'PATCH']:
            self.fields.pop('username')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = f"{instance.first_name} {instance.last_name}".strip()
        return ret

    def to_internal_value(self, data):
        internal = super().to_internal_value(data)
        name = data.get('name', '')
        parts = name.split()
        internal['first_name'] = parts[0] if len(parts) >= 1 else ''
        internal['last_name'] = ' '.join(parts[1:]) if len(parts) > 1 else ''
        return internal

    #gpt
class UserSerializerForPUT(serializers.ModelSerializer):
    name = serializers.CharField()
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'address', 'name', 'gender']
        read_only_fields = ['username']
        extra_kwargs = {
            'email': {'required': True},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = f"{instance.first_name} {instance.last_name}".strip()
        return ret

    def to_internal_value(self, data):
        internal = super().to_internal_value(data)
        name = data.get('name', '')
        parts = name.split()
        internal['first_name'] = parts[0] if len(parts) >= 1 else ''
        internal['last_name'] = ' '.join(parts[1:]) if len(parts) > 1 else ''
        return internal


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()