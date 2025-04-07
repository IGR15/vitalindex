from django.urls import path
from patients.api.views import (
    CreatePatient, PatientList, PatientDetail, PatientDetailByName
)

urlpatterns = [
    path('patients/', PatientList.as_view(), name='patient-list'), 
    path('patients/create/', CreatePatient.as_view(), name='create-patient'), 
    path('patients/<int:pk>/', PatientDetail.as_view(), name='patient-detail'),
    path('patients/search/', PatientDetailByName.as_view(), name='patient-search'), 
]
