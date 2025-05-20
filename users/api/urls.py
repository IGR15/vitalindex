from django.urls import path
from users.api.views import (
    UserList, UserDetail, UserByRole, SingleUserByRole, UserCreate, RoleDetail,
    CustomTokenObtainPairView  ,LogoutView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # JWT Auth
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/users/logout/', LogoutView.as_view(), name='logout'),


    # User APIs
    path('users/', UserList.as_view(), name='user-list'), 
    path('users/create/', UserCreate.as_view(), name='user-create'), 
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),  
    path('users/role/<int:role_id>/', UserByRole.as_view(), name='users-by-role'), 
    path('users/role/<int:role_id>/<int:user_id>/', SingleUserByRole.as_view(), name='single-user-by-role'),  

    # Permissions APIs
    # path('permissions/', PermissionsList.as_view(), name='permissions-list'), 
    # path('permissions/create/', CreatePermission.as_view(), name='create-permission'),  
    # path('permissions/<int:pk>/', Permissions.as_view(), name='permission-detail'),  

    # Roles APIs
    # path('roles/', RoleList.as_view(), name='roles-list'),  
    # path('roles/create/', CreateRole.as_view(), name='create-role'),  
    path('roles/<int:pk>/', RoleDetail.as_view(), name='role-detail'), 
]
