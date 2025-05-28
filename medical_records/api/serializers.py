from rest_framework import serializers
from medical_records.models import MedicalRecord,Vital
from patients.api.serializers import PatientSerializer
from patients.models import Patient

class VitalsInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital
        fields = [
            'id',
            'temperature',
            'heart_rate',
            'blood_pressure',
            'oxygen_saturation',
            'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']

        
class VitalsCreateSerializer(serializers.ModelSerializer):
    medical_record_id = serializers.PrimaryKeyRelatedField(
        queryset=MedicalRecord.objects.all(),
        source='medical_record',
        write_only=True
    )

    class Meta:
        model = Vital
        fields = [
            'id',
            'medical_record_id',
            'temperature',
            'heart_rate',
            'blood_pressure',
            'oxygen_saturation',
            'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class PatientBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        source='patient',
        write_only=True,
    )
    patient_name = serializers.SerializerMethodField(read_only=True)
    vitals = VitalsInlineSerializer(many=True, required=False)

    class Meta:
        model = MedicalRecord
        fields = [
            'record_id',
            'patient_id',
            'patient_name', 
            'created_date',
            'last_updated',
            'diagnosis',
            'treatment_plan',
            'observations',
            'is_public',
            'vitals'
        ]

    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def create(self, validated_data):
        vitals_data = validated_data.pop('vitals', [])
        patient = validated_data.get('patient')
        if not patient:
            raise serializers.ValidationError({"patient_id": "This field is required."})

        medical_record = MedicalRecord.objects.create(**validated_data)
        for vital in vitals_data:
            Vital.objects.create(medical_record=medical_record, **vital)
        return medical_record

    
class MedicalRecordUpdateSerializer(serializers.ModelSerializer):
    vitals = VitalsInlineSerializer(many=True, required=False)

    class Meta:
        model = MedicalRecord
        fields = [
            'record_id', 'diagnosis',
            'treatment_plan', 'observations', 'is_public', 'vitals'
        ]

    def update(self, instance, validated_data):
        vitals_data = validated_data.pop('vitals', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if vitals_data is not None:
            instance.vitals.all().delete()
            for vital in vitals_data:
                Vital.objects.create(medical_record=instance, **vital)

        return instance



class RedactedMedicalRecordSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    vitals = MedicalRecordSerializer(many=True, read_only=True)  

    class Meta:
        model = MedicalRecord
        exclude = ['patient'] 

    def get_name(self, obj):
        return "John Doe"

    
