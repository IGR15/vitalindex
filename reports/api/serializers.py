from rest_framework import serializers
from reports.models import Report
from patients.api.serializers import PatientSerializer
from staff.api.serializers import DoctorSerializer



class ReportSerializer(serializers.ModelSerializer):
    patient=PatientSerializer(read_only=True)
    doctor=DoctorSerializer(read_only=True)
    class Meta:
        model = Report
        fields = '__all__'
