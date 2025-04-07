from django.urls import path
from users.api.views import (
    UserList, UserDetail, UserByRole, SingleUserByRole, UserCreate,
    PermissionsList, CreatePermission, Permissions,
    RoleList, CreateRole, RoleDetail
)

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'), 
    path('users/create/', UserCreate.as_view(), name='user-create'), 
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),  
    path('users/role/<int:role_id>/', UserByRole.as_view(), name='users-by-role'), 
    path('users/role/<int:role_id>/<int:user_id>/', SingleUserByRole.as_view(), name='single-user-by-role'),  

    path('permissions/', PermissionsList.as_view(), name='permissions-list'), 
    path('permissions/create/', CreatePermission.as_view(), name='create-permission'),  
    path('permissions/<int:pk>/', Permissions.as_view(), name='permission-detail'),  

    path('roles/', RoleList.as_view(), name='roles-list'),  
    path('roles/create/', CreateRole.as_view(), name='create-role'),  
    path('roles/<int:pk>/', RoleDetail.as_view(), name='role-detail'), 
]
