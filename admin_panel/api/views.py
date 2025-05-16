from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from patients.models import Patient
import psutil
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

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

@method_decorator(name='get', decorator=swagger_auto_schema(tags=['admin_panel']))
class SystemStatsView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users allowed
    permission_classes = [IsAdminUser]  # Only admin/staff users allowed

    def get(self, request):
        user_count = User.objects.filter(is_active=True).count()
        patient_count = Patient.objects.count()
        logged_in_users = get_logged_in_users()

        # Server info
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        uptime_seconds = int(now().timestamp() - psutil.boot_time())

        return Response({
            "user_count": user_count,
            "logged_in_user_count": logged_in_users.count(),
            "logged_in_users": [user.username for user in logged_in_users],
            "patient_count": patient_count,
            "server_status": {
                "cpu_usage_percent": cpu_usage,
                "ram_usage_percent": ram_usage,
                "uptime_seconds": uptime_seconds
            }
        })
