from django.urls import path
from medical_records.api.views import (
    CreateMedicalRecord,
    CreateVitals,
    MedicalRecordDetail,
    VitalsDetail, 
    MedicalRecordsByPatientAPIView,
    EducationalRecordsView, 
    SingleEducationalRecordView,
    MedicalRecordByPatient,
    MedicalRecordByPatientName,
)

urlpatterns = [
    path('medical-records/', MedicalRecordsByPatientAPIView.as_view(), name='medical-records-by-patient'),  
    path('medical-records/create/', CreateMedicalRecord.as_view(), name='create-medical-record'),  
    path('medical-records/<int:record_id>/', MedicalRecordDetail.as_view(), name='medical-record-detail'),  
    path('vitals/create/', CreateVitals.as_view(), name='create-vitals'),  
    path('vitals/<int:pk>/', VitalsDetail.as_view(), name='vitals-detail'), 
    path('educational/', EducationalRecordsView.as_view(), name='educational-records'),
    path('educational/<int:pk>/', SingleEducationalRecordView.as_view(), name='educational-record-detail'),
    path('medical-records/patient/<int:patient_id>/', MedicalRecordByPatient.as_view(), name='medical-records-by-patient-id'),
    path('medical-records/patient-name/<str:patient_name>/', MedicalRecordByPatientName.as_view(), name='medical-records-by-patient-name'),
]
