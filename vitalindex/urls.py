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

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('alerts/', include('alerts.api.urls')),  # Alerts app
    path('education/', include('education.api.urls')),  # Education app
    path('hospital/', include('hospital.api.urls')),  # Hospital app
    path('medical-records/', include('medical_records.api.urls')),  # Medical Records app
    path('patients/', include('patients.api.urls')),  # Patients app
    path('reports/', include('reports.api.urls')),  # Reports app
    path('staff/', include('staff.api.urls')),  # Staff app (Doctors, Nurses, etc.)
    path('users/', include('users.api.urls')),  # User Authentication & Management
]
