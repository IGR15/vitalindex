from rest_framework import serializers
from reports.models import Report
# from education.models import CaseStudy
from patients.models import Patient

class ReportSearchSerializer(serializers.ModelSerializer):
    similarity = serializers.FloatField()

    class Meta:
        model = Report
        fields = ['report_id', 'report_title', 'similarity']

# class CaseStudySearchSerializer(serializers.ModelSerializer):
#     similarity = serializers.FloatField()

#     class Meta:
#         model = CaseStudy
#         fields = ['case_id', 'case_title', 'similarity']

class PatientSearchSerializer(serializers.ModelSerializer):
    similarity = serializers.FloatField()

    class Meta:
        model = Patient
        fields = ['patient_id', 'first_name', 'last_name', 'similarity']
