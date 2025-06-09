from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils.timezone import now, timedelta
from django.db.models import Count, Q
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from patients.models import Patient
from reports.models import Report
from medical_records.models import MedicalRecord
from staff.models import Doctor, Nurse, Student
import psutil
import shutil
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from admin_panel.api.serializers import (
    SystemStatsSerializer,
    ServerStatusSerializer,
    UserActivitySerializer,
    UserRoleStatsSerializer,
    ActivityLogSerializer
)

User = get_user_model()

def get_logged_in_users():
    active_sessions = Session.objects.filter(expire_date__gte=now())
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            user_ids.append(user_id)
    return User.objects.filter(id__in=user_ids)

def format_uptime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    return f"{days}d {hours}h {minutes}m"


class SystemStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    swagger_auto_schema(tags=['Admin Panel'])
    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        logged_in_users = get_logged_in_users()

        total_patients = Patient.objects.count()
        total_reports = Report.objects.count()
        total_medical_records = MedicalRecord.objects.count()
        total_doctors = Doctor.objects.count()
        total_nurses = Nurse.objects.count()
        total_students = Student.objects.count()

        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = shutil.disk_usage('/').used / shutil.disk_usage('/').total * 100
        uptime_seconds = int(now().timestamp() - psutil.boot_time())

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = "healthy"
        except Exception:
            db_status = "error"

        stats_data = {
            "total_users": total_users,
            "active_users": active_users,
            "total_patients": total_patients,
            "total_reports": total_reports,
            "total_medical_records": total_medical_records,
            "total_doctors": total_doctors,
            "total_nurses": total_nurses,
            "total_students": total_students,
            "logged_in_users": logged_in_users.count(),
        }

        server_data = {
            "cpu_usage_percent": cpu_usage,
            "ram_usage_percent": ram_usage,
            "disk_usage_percent": round(disk_usage, 2),
            "uptime_seconds": uptime_seconds,
            "uptime_formatted": format_uptime(uptime_seconds),
            "server_time": now(),
            "database_status": db_status
        }

        return Response({
            "system_stats": SystemStatsSerializer(stats_data).data,
            "server_status": ServerStatusSerializer(server_data).data,
            "logged_in_users": [
                UserActivitySerializer({
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role or "Admin" if user.is_superuser else "Unknown",
                    "last_login": user.last_login,
                    "is_active": user.is_active,
                    "date_joined": user.date_joined,
                    "login_count": 0
                }).data for user in logged_in_users
            ]
        })

class UserActivityView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    swagger_auto_schema(tags=['Admin Panel'])
    def get(self, request):
        days = int(request.GET.get('days', 30))
        role_filter = request.GET.get('role', None)

        start_date = now() - timedelta(days=days)
        users_queryset = User.objects.all()

        if role_filter:
            users_queryset = users_queryset.filter(role=role_filter)

        users_data = []
        for user in users_queryset:
            reports_count = Report.objects.filter(
                created_by=user,
                created_at__gte=start_date
            ).count()

            records_count = MedicalRecord.objects.filter(
                created_by=user,
                created_at__gte=start_date
            ).count()

            users_data.append({
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role or "Admin" if user.is_superuser else "Unknown",
                "last_login": user.last_login,
                "is_active": user.is_active,
                "date_joined": user.date_joined,
                "login_count": reports_count + records_count
            })

        return Response({
            "period_days": days,
            "total_users": len(users_data),
            "users": UserActivitySerializer(users_data, many=True).data
        })

class UserRoleStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    swagger_auto_schema(tags=['Admin Panel'])
    def get(self, request):
        total_users = User.objects.count()

        role_stats = User.objects.values('role').annotate(
            count=Count('role')
        ).order_by('-count')

        admin_count = User.objects.filter(is_superuser=True).count()

        role_data = []
        for stat in role_stats:
            role = stat['role'] or 'Unknown'
            count = stat['count']
            percentage = (count / total_users * 100) if total_users > 0 else 0

            role_data.append({
                "role": role,
                "count": count,
                "percentage": round(percentage, 2)
            })

        if admin_count > 0:
            admin_percentage = (admin_count / total_users * 100) if total_users > 0 else 0
            role_data.append({
                "role": "Admin",
                "count": admin_count,
                "percentage": round(admin_percentage, 2)
            })

        return Response({
            "total_users": total_users,
            "role_distribution": UserRoleStatsSerializer(role_data, many=True).data
        })

class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    swagger_auto_schema(tags=['Admin Panel'])
    def get(self, request):
        limit = int(request.GET.get('limit', 50))

        activities = []

        recent_reports = Report.objects.select_related('doctor', 'patient').order_by('-created_at')[:limit//2]
        for report in recent_reports:
            activities.append({
                "timestamp": report.created_at,
                "user": report.doctor.user.username if report.doctor else "System",
                "action": "Created Report",
                "resource": f"Report #{report.report_id}",
                "details": f"Report for patient: {report.patient.first_name} {report.patient.last_name}"
            })

        recent_records = MedicalRecord.objects.select_related('patient').order_by('-created_at')[:limit//2]
        for record in recent_records:
            activities.append({
                "action": "Created Medical Record",
                "resource": f"Record #{record.record_id}",
                "details": f"Medical record for patient: {record.patient.first_name} {record.patient.last_name}"
            })

        activities.sort(key=lambda x: x['timestamp'], reverse=True)

        return Response({
            "activities": ActivityLogSerializer(activities[:limit], many=True).data,
            "total_shown": min(len(activities), limit)
        })

class ServerHealthView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    swagger_auto_schema(tags=['Admin Panel'])
    def get(self, request):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = shutil.disk_usage('/')

            network = psutil.net_io_counters()
            process_count = len(psutil.pids())

            try:
                load_avg = psutil.getloadavg()
            except AttributeError:
                load_avg = [0, 0, 0]

            health_status = "healthy"
            if cpu_percent > 80 or memory.percent > 85:
                health_status = "warning"
            if cpu_percent > 95 or memory.percent > 95:
                health_status = "critical"

            return Response({
                "overall_status": health_status,
                "cpu": {
                    "usage_percent": cpu_percent,
                    "load_average": {
                        "1min": load_avg[0],
                        "5min": load_avg[1],
                        "15min": load_avg[2]
                    }
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "usage_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "usage_percent": round((disk.used / disk.total) * 100, 2)
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_received": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_received": network.packets_recv
                },
                "processes": {
                    "total_count": process_count
                },
                "uptime": {
                    "seconds": int(now().timestamp() - psutil.boot_time()),
                    "formatted": format_uptime(int(now().timestamp() - psutil.boot_time()))
                }
            })

        except Exception as e:
            return Response({
                "error": "Failed to retrieve server health data",
                "details": str(e)
            }, status=500)
