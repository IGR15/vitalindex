from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.permissions import IsAdminOrDoctorOrNurse, IsAdminOrDoctor
from rest_framework.permissions import IsAuthenticated
from reports.models import Report
from staff.models import Doctor
from patients.models import Patient
from reports.api.serializers import ReportSerializer, ReportSerializerForPOST, ReportSerializerForPUT
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from notifications.handlers import send_message
from users.models import User

class CreateReport(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(request_body=ReportSerializerForPOST, tags=['Reports'])
    def post(self, request):
        try:
            serializer = ReportSerializerForPOST(data=request.data, context={'request': request})

            if serializer.is_valid():
                report = serializer.save(doctor=request.user.doctor)

                
                doctors = User.objects.filter(role='Doctor')
                for doctor in doctors:
                    send_message(
                        f"New report published by Dr. {request.user.username}",
                        doctor,
                        'report_published'
                    )

                response_serializer = ReportSerializer(report, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportList(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['Reports'])
    def get(self, request):
        try:
            reports = Report.objects.all()
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['Reports'])
    def get(self, request, report_id):
        try:
            report = get_object_or_404(Report, report_id=report_id)
            report.total_views += 1
            report.viewed_by.add(request.user)  
            report.save()
            serializer = ReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ReportSerializerForPUT, tags=['Reports'])
    def put(self, request, report_id):
        try:
            report = get_object_or_404(Report, report_id=report_id)

            if request.user.role == 'Doctor' and getattr(request.user, 'doctor', None) != report.doctor:
                return Response(
                    {"error": "You do not have permission to modify this report."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ReportSerializerForPUT(report, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['Reports'])
    def delete(self, request, report_id):
        try:
            report = get_object_or_404(Report, report_id=report_id)

            if request.user.role == 'Doctor' and getattr(request.user, 'doctor', None) != report.doctor:
                return Response(
                    {"error": "You do not have permission to modify this report."},
                    status=status.HTTP_403_FORBIDDEN
                )

            report.delete()
            return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportByPatient(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    patient_param = openapi.Parameter(
        'patient_name', openapi.IN_QUERY,
        description="Patient's first name to filter reports",
        type=openapi.TYPE_STRING,
        required=True
    )

    @swagger_auto_schema(manual_parameters=[patient_param], tags=['Reports'])
    def get(self, request):
        try:
            patient_name = request.query_params.get('patient_name')

            if not patient_name:
                return Response({"error": "Parameter 'patient_name' is required."}, status=status.HTTP_400_BAD_REQUEST)

            reports = Report.objects.filter(patient__first_name__icontains=patient_name)
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportByDoctor(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    doctor_param = openapi.Parameter(
        'doctor_name', openapi.IN_QUERY,
        description="Doctor's username to filter reports",
        type=openapi.TYPE_STRING,
        required=True
    )

    @swagger_auto_schema(manual_parameters=[doctor_param], tags=['Reports'])
    def get(self, request):
        try:
            doctor_name = request.query_params.get('doctor_name')

            if not doctor_name:
                return Response({"error": "Parameter 'doctor_name' is required."}, status=status.HTTP_400_BAD_REQUEST)

            reports = Report.objects.filter(doctor__user__username__icontains=doctor_name)
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PublicReportsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Reports'])
    def get(self, request):
        try:
            public_reports = Report.objects.filter(is_public=True)
            serializer = ReportSerializer(public_reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportViewCountView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['Reports'])
    def get(self, request, report_id):
        try:
            report = get_object_or_404(Report, report_id=report_id)

            view_count = report.total_views 

            return Response(
                {"report_id": report_id, "view_count": view_count},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class RecordViewReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['Reports'])
    def post(self, request, report_id):
        try:
            report = get_object_or_404(Report, report_id=report_id)
            user = request.user
            report.viewed_by.add(user)
            report.total_views += 1
            report.save()

            return Response(
                {"message": f"User {user.username} viewed report {report_id}.", "total_views": report.total_views},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



