from django.urls import path
from medical_records.api.views import (
    CreateMedicalRecord,
    CreateVitals,
    MedicalRecordDetail,
    VitalsDetail, 
    GetAllMedicalRecords,
    MedicalRecordByPatient,
    MedicalRecordByPatientName,
)

urlpatterns = [
    path('medical-records/', GetAllMedicalRecords.as_view(), name='get-all-medical-records'),  
    path('medical-records/create/', CreateMedicalRecord.as_view(), name='create-medical-record'),  
    path('medical-records/<int:record_id>/', MedicalRecordDetail.as_view(), name='medical-record-detail'),  
    path('vitals/create/', CreateVitals.as_view(), name='create-vitals'),  
    path('vitals/<int:pk>/', VitalsDetail.as_view(), name='vitals-detail'), 
    path('medical-records/patient/<int:patient_id>/', MedicalRecordByPatient.as_view(), name='medical-records-by-patient-id'),
    path('medical-records/patient-name/<str:patient_name>/', MedicalRecordByPatientName.as_view(), name='medical-records-by-patient-name'),
]
