from rest_framework import serializers
from reports.models import Report
from staff.models import Doctor
from users.models import User
from patients.models import Patient
from medical_records.models import MedicalRecord

class ReportSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.username', read_only=True)

    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient')
    medical_record_id = serializers.PrimaryKeyRelatedField(queryset=MedicalRecord.objects.all(), source='medical_record', required=False, allow_null=True)
    modified_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='modified_by', required=False, allow_null=True)

    reviewed_by_ids = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    reviewed_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Report
        fields = [
            'report_id',
            'doctor_id',  # <== Now you will see doctor_id in GET ✅
            'doctor_name',  # <== Optional: shows name
            'patient_id',
            'medical_record_id',
            'report_title',
            'report_type',
            'report_content',
            'report_file',
            'doctor_signature',
            'reviewed_by_ids',
            'reviewed_by',
            'is_public',
            'keywords',
            'related_studies',
            'version',
            'modified_by_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['version', 'created_at', 'updated_at']

    def create(self, validated_data):
        reviewed_by = validated_data.pop('reviewed_by_ids', [])
        report = Report.objects.create(**validated_data)
        if reviewed_by:
            report.reviewed_by.set(reviewed_by)
        return report

    def update(self, instance, validated_data):
        reviewed_by = validated_data.pop('reviewed_by', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if reviewed_by is not None:
            instance.reviewed_by.set(reviewed_by)

        instance.version += 1
        instance.save()
        return instance
