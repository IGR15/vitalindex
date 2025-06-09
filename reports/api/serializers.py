from rest_framework import serializers
from reports.models import Report
from staff.models import Doctor
from users.models import User
from patients.models import Patient
from medical_records.models import MedicalRecord

class ReportSerializerForPOST(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient')
    available_medical_records = serializers.ListField(child=serializers.DictField(), read_only=True)

    class Meta:
        model = Report
        fields = [
            'patient_id',
            'available_medical_records',
            'report_title',
            'report_type',
            'report_content',
            'report_file',
            'doctor_signature',
            'is_public',
            'related_studies'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            patient_id = request.data.get('patient_id')
            if patient_id:
                records = MedicalRecord.objects.filter(patient_id=patient_id).values('pk', 'diagnosis', 'created_date')
                self.fields['available_medical_records'].default = [
                    {
                        'id': r['pk'],
                        'diagnosis': r['diagnosis'],
                        'created_date': r['created_date']
                    } for r in records
                ]
            else:
                self.fields['available_medical_records'].default = []

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if not user or not hasattr(user, 'doctor'):
            raise serializers.ValidationError('Only doctors can create reports.')

        validated_data['doctor'] = user.doctor

        # Set the first medical record automatically
        patient = validated_data['patient']
        first_record = MedicalRecord.objects.filter(patient=patient).first()
        validated_data['medical_record'] = first_record

        # Set keywords as empty for now
        validated_data['keywords'] = ''

        report = Report.objects.create(**validated_data)
        return report



class ReportSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.username', read_only=True)

    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient')
    patient_name = serializers.SerializerMethodField()

    medical_record_id = serializers.PrimaryKeyRelatedField(queryset=MedicalRecord.objects.all(), source='medical_record', required=False, allow_null=True)

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
            'viewed_by',
            'is_public',
            'keywords',
            'related_studies',
            'version',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['version', 'created_at', 'updated_at']

    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

class ReportSerializerForPUT(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient')
    medical_record_id = serializers.PrimaryKeyRelatedField(queryset=MedicalRecord.objects.all(), source='medical_record', required=False, allow_null=True)

    class Meta:
        model = Report
        fields = [
            'patient_id',
            'medical_record_id',
            'report_title',
            'report_type',
            'report_content',
            'report_file',
            'doctor_signature',
            'is_public',
            'related_studies'
        ]

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

    
        if user and user.role == 'Doctor' and hasattr(user, 'doctor'):
            if instance.doctor != user.doctor:
                raise serializers.ValidationError('You do not have permission to modify this report.')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.version += 1
        instance.save()
        return instance



# class ReportSerializer(serializers.ModelSerializer):
#     doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', read_only=True)
#     doctor_name = serializers.CharField(source='doctor.user.username', read_only=True)

#     patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient')
#     patient_name = serializers.SerializerMethodField()

#     medical_record_id = serializers.PrimaryKeyRelatedField(queryset=MedicalRecord.objects.all(), source='medical_record', required=False, allow_null=True)

#     # by default define it here:
#     viewed_by_ids = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         many=True,
#         required=False,
#         write_only=True
#     )
#     viewed_by = serializers.StringRelatedField(many=True, read_only=True)

#     class Meta:
#         model = Report
#         fields = [
#             'report_id',
#             'doctor_id',
#             'doctor_name',
#             'patient_id',
#             'patient_name',
#             'medical_record_id',
#             'report_title',
#             'report_type',
#             'report_content',
#             'report_file',
#             'doctor_signature',
#             'viewed_by_ids',
#             'viewed_by',
#             'is_public',
#             'keywords',
#             'related_studies',
#             'version',
#             'created_at',
#             'updated_at',
#         ]
#         read_only_fields = ['version', 'created_at', 'updated_at']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         request = self.context.get('request', None)
#         if request:
#             method = request.method
#             if method == 'POST':
#                 self.fields.pop('viewed_by_ids')

#     def get_patient_name(self, obj):
#         return f"{obj.patient.first_name} {obj.patient.last_name}"

#     def create(self, validated_data):
#         viewed_by = validated_data.pop('viewed_by_ids', [])
#         report = Report.objects.create(**validated_data)
#         if viewed_by:
#             report.viewed_by.set(viewed_by)
#         return report

#     def update(self, instance, validated_data):
#         request = self.context.get('request')
#         user = getattr(request, 'user', None)

#         if user and user.role == 'Doctor' and hasattr(user, 'doctor'):
#             if instance.doctor != user.doctor:
#                 raise serializers.ValidationError(
#                     'You do not have permission to modify this report.'
#                 )

#         viewed_by = validated_data.pop('viewed_by_ids', None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         if viewed_by is not None:
#             instance.viewed_by.set(viewed_by)

#         instance.version += 1
#         if user:
#             instance.modified_by = user
#         instance.save()
#         return instance
