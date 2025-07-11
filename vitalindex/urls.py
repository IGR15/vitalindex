"""
URL configuration for vitalindex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
schema_view = get_schema_view(
    openapi.Info(
        title="VitalIndex API",
        default_version='v1',
        description="API documentation for the VitalIndex hospital system",
        terms_of_service="https://www.yourhospital.com/terms/",
        contact=openapi.Contact(email="admin@vitalindex.ps"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),  
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/', include('core.api.urls')),
    
    
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/admin_panel/', include('admin_panel.api.urls')),

    path('api/v1/alerts/', include('alerts.api.urls')),
    path('api/v1/education/', include('education.api.urls')),
    path('api/v1/hospital/', include('hospital.api.urls')),
    path('api/v1/medical-records/', include('medical_records.api.urls')),
    path('api/v1/patients/', include('patients.api.urls')),
    path('api/v1/reports/', include('reports.api.urls')),
    path('api/v1/staff/', include('staff.api.urls')),
    path('api/v1/users/', include('users.api.urls')),
    path('api/v1/core/', include('api.urls')), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

