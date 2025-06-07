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
    patient_name = serializers.SerializerMethodField()

    medical_record_id = serializers.PrimaryKeyRelatedField(queryset=MedicalRecord.objects.all(), source='medical_record', required=False, allow_null=True)

    # by default define it here:
    viewed_by_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
        write_only=True
    )
    viewed_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Report
        fields = [
            'report_id',
            'doctor_id',
            'doctor_name',
            'patient_id',
            'patient_name',
            'medical_record_id',
            'report_title',
            'report_type',
            'report_content',
            'report_file',
            'doctor_signature',
            'viewed_by_ids',
            'viewed_by',
            'is_public',
            'keywords',
            'related_studies',
            'version',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['version', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request:
            method = request.method
            if method == 'POST':
                self.fields.pop('viewed_by_ids')

    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def create(self, validated_data):
        viewed_by = validated_data.pop('viewed_by_ids', [])
        report = Report.objects.create(**validated_data)
        if viewed_by:
            report.viewed_by.set(viewed_by)
        return report

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user and user.role == 'Doctor' and hasattr(user, 'doctor'):
            if instance.doctor != user.doctor:
                raise serializers.ValidationError(
                    'You do not have permission to modify this report.'
                )

        viewed_by = validated_data.pop('viewed_by_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if viewed_by is not None:
            instance.viewed_by.set(viewed_by)

        instance.version += 1
        if user:
            instance.modified_by = user
        instance.save()
        return instance
