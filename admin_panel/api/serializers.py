from rest_framework import serializers
from django.contrib.auth import get_user_model
from patients.models import Patient
from reports.models import Report
from medical_records.models import MedicalRecord
from staff.models import Doctor, Nurse, Student

User = get_user_model()

class UserActivitySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()
    role = serializers.CharField()
    last_login = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField()
    login_count = serializers.IntegerField()

class SystemStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_patients = serializers.IntegerField()
    total_reports = serializers.IntegerField()
    total_medical_records = serializers.IntegerField()
    total_doctors = serializers.IntegerField()
    total_nurses = serializers.IntegerField()
    total_students = serializers.IntegerField()
    logged_in_users = serializers.IntegerField()

class ServerStatusSerializer(serializers.Serializer):
    cpu_usage_percent = serializers.FloatField()
    ram_usage_percent = serializers.FloatField()
    disk_usage_percent = serializers.FloatField()
    uptime_seconds = serializers.IntegerField()
    uptime_formatted = serializers.CharField()
    server_time = serializers.DateTimeField()
    database_status = serializers.CharField()

class UserRoleStatsSerializer(serializers.Serializer):
    role = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()

class ActivityLogSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    user = serializers.CharField()
    action = serializers.CharField()
    resource = serializers.CharField()
    details = serializers.CharField()
