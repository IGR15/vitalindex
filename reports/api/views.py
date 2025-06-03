from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.permissions import IsAdminOrDoctorOrNurse, IsAdminOrDoctor
from rest_framework.permissions import IsAuthenticated
from reports.models import Report
from staff.models import Doctor
from patients.models import Patient
from reports.api.serializers import ReportSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from notifications.handlers import send_message
from users.models import User

class CreateReport(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(request_body=ReportSerializer, tags=['Reports'])
    def post(self, request):
        try:
            serializer = ReportSerializer(data=request.data)

            if serializer.is_valid():
                report = serializer.save(doctor=request.user.doctor)
                doctors = User.objects.filter(role='Doctor')
                for doctor in doctors:
                    send_message(
                        f"New report published by Dr. {request.user.username}",
                        doctor,
                        'report_published'
                    )

                return Response(serializer.data, status=status.HTTP_201_CREATED)

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
            serializer = ReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ReportSerializer, tags=['Reports'])
    def put(self, request, report_id):
        try:
            report = get_object_or_404(Report, report_id=report_id)
            serializer = ReportSerializer(report, data=request.data, partial=True)
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
            report.delete()
            return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportByPatient(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['Reports'])
    def get(self, request):
        try:
            patient_id = request.query_params.get('patient_id')
            patient_name = request.query_params.get('patient_name')

            if patient_id:
                reports = Report.objects.filter(patient__patient_id=patient_id)
            elif patient_name:
                reports = Report.objects.filter(patient__first_name__icontains=patient_name)
            else:
                return Response({"error": "Provide patient_id or patient_name"}, status=status.HTTP_400_BAD_REQUEST)

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


class ReviewedReportsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['Reports'])
    def get(self, request, doctor_id):
        try:
            doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
            reports = Report.objects.filter(reviewed_by=doctor)
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
