from rest_framework import serializers
from patients.models import Patient

class PatientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()  
    class Meta:
        model = Patient
        fields = ['id', 'name', 'gender', 'address', 'phone', 'email', 'medical_history', 'date_of_birth']
