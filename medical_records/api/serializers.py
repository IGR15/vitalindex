from rest_framework import serializers
from medical_records.models import MedicalRecord,Vital
from patients.api.serializers import PatientSerializer
from patients.models import Patient

class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = ['id', 'temperature', 'heart_rate', 'blood_pressure', 'oxygen_saturation', 'timestamp']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='patient', write_only=True
    )
    patient = PatientSerializer(read_only=True)
    vitals = VitalsSerializer(many=True, required=False)

    class Meta:
        model = MedicalRecord
        fields = [
            'record_id', 'patient_id', 'patient',  # Include patient only for GET
            'created_date', 'last_updated',
            'diagnosis', 'treatment_plan',
            'observations', 'vitals'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide 'patient' if this is a write operation (input)
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            self.fields.pop('patient')





class RedactedMedicalRecordSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    vitals = VitalsSerializer(many=True, read_only=True)  

    class Meta:
        model = MedicalRecord
        exclude = ['patient'] 

    def get_name(self, obj):
        return "John Doe"

    
