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


class IsAdmin(HasMinimumRolePermission):
    required_level = 4


class IsAdminOrDoctor(HasMinimumRolePermission):
    required_level = 3  


class IsAdminOrDoctorOrNurse(HasMinimumRolePermission):
    required_level = 2  


class IsAdminOrDoctorOrStudent(BasePermission):
    def has_permission(self, request, view):
        return check_user_permission_level(request.user, 1) and request.user.role in ['Student', 'Doctor', 'Admin']


class IsAdminOrDoctorOrNurseOrStudent(HasMinimumRolePermission):
    required_level = 1 
    
# All roles permitted
# from rest_framework.permissions import BasePermission
# from users.utiles import check_user_permission_level

# class HasMinimumRolePermission(BasePermission):
#     required_level = 1

#     def has_permission(self, request, view):
#         return check_user_permission_level(request.user, self.required_level)

# class IsStudent(HasMinimumRolePermission):
#     required_level = 1

# class IsNurse(HasMinimumRolePermission):
#     required_level = 2

# class IsDoctor(HasMinimumRolePermission):
#     required_level = 3
