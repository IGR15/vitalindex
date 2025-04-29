from rest_framework import serializers
from medical_records.models import MedicalRecord,Vital
from patients.api.serializers import PatientSerializer

class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = ['id', 'temperature', 'heart_rate', 'blood_pressure', 'oxygen_saturation', 'timestamp']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patiant=PatientSerializer(read_only=True)
    vitals = VitalsSerializer(read_only=True) 

    class Meta:
        model = MedicalRecord
        fields = ['record_id', 'patient', 'created_date', 'last_updated', 'diagnosis', 'treatment_plan', 'observations', 'vitals']

    def create(self, validated_data):
        """
        Create a medical record and optionally its vitals.
        """
        vitals_data = validated_data.pop('vitals', None)
        medical_record = MedicalRecord.objects.create(**validated_data)

        if vitals_data:
            Vital.objects.create(record=medical_record, **vitals_data)
        
        return medical_record
