from rest_framework.permissions import BasePermission
from users.utiles import check_user_permission_level

class HasMinimumRolePermission(BasePermission):
    required_level = 1

    def has_permission(self, request, view):
        return check_user_permission_level(request.user, self.required_level)

class IsStudent(HasMinimumRolePermission):
    required_level = 1

class IsNurse(HasMinimumRolePermission):
    required_level = 2

class IsDoctor(HasMinimumRolePermission):
    required_level = 3
