from rest_framework import serializers
from medical_records.models import MedicalRecord,Vital
from patients.api.serializers import PatientSerializer

class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = ['id', 'temperature', 'heart_rate', 'blood_pressure', 'oxygen_saturation', 'timestamp']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient=PatientSerializer(read_only=True)
    vitals = VitalsSerializer(many=True, required=False)

    class Meta:
        model = MedicalRecord
        fields = ['record_id', 'patiant', 'created_date', 'last_updated', 'diagnosis', 'treatment_plan', 'observations', 'vitals']

    def create(self, validated_data):
        vitals_data = validated_data.pop('vitals', [])
        medical_record = MedicalRecord.objects.create(**validated_data)

        for vital in vitals_data:
            Vital.objects.create(record=medical_record, **vital)

        return medical_record


class RedactedMedicalRecordSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    vitals = VitalsSerializer(many=True, read_only=True)  

    class Meta:
        model = MedicalRecord
        exclude = ['patient'] 

    def get_name(self, obj):
        return "John Doe"

    
