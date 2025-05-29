from rest_framework import serializers
from medical_records.models import MedicalRecord
from medical_records.api.serializers import VitalsInlineSerializer

class RedactedMedicalRecordSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    vitals = VitalsInlineSerializer(many=True, read_only=True)  
    class Meta:
        model = MedicalRecord
        exclude = ['patient']

    def get_name(self, obj):
        return "John Doe"