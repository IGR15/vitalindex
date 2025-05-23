from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.permissions import (IsAdminOrDoctorOrNurse,IsAdminOrDoctor)
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from reports.models import Report
from staff.models import Doctor
from patients.models import Patient
from reports.api.serializers import ReportSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateReport(APIView):
    permission_classes=[IsAuthenticated,IsAdminOrDoctor]
    @swagger_auto_schema(request_body=ReportSerializer,tags=['Reports'])
    def post(self, request):
        try:
            patient = get_object_or_404(Patient, patient_id=request.data['patient_id'])
            doctor = get_object_or_404(Doctor, doctor_id=request.data['doctor_id'])
            serializer = ReportSerializer(data=request.data)
        except Patient.DoesNotExist or Doctor.DoesNotExist:    
            return Response({'error': 'Patient or Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(patient=patient, doctor=doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportList(APIView):
    permission_classes=[IsAuthenticated,IsAdminOrDoctorOrNurse]
    @swagger_auto_schema(tags=['Reports'])
    def get(self, request):
        try:
            reports = Report.objects.all()
        except Report.DoesNotExist:
            return Response({'error': 'Reports not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

class ReportDetail(APIView):
    permission_classes=[IsAuthenticated,IsAdminOrDoctorOrNurse]
    @swagger_auto_schema(tags=['Reports'])
    def get(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=ReportSerializer,tags=['Reports'])
    def put(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(tags=['Reports'])
    def delete(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        report.delete()
        return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ReportByPatient(APIView):
    permission_classes=[IsAuthenticated,IsAdminOrDoctorOrNurse]
    @swagger_auto_schema(tags=['Reports'])
    def get(self, request):
        patient_id = request.query_params.get('patient_id')
        patient_name = request.query_params.get('patient_name')

        if patient_id:
            reports = Report.objects.filter(patient__patient_id=patient_id)
        elif patient_name:
            reports = Report.objects.filter(patient__name__icontains=patient_name)
        else:
            return Response({"error": "Please provide either patient_id or patient_name"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(tags=['Reports'])
    def put(self, request):
        patient_id = request.query_params.get('patient_id')
        patient_name = request.query_params.get('patient_name')

        if patient_id:
            report = get_object_or_404(Report, patient__patient_id=patient_id)
        elif patient_name:
            report = get_object_or_404(Report, patient__name__icontains=patient_name)
        else:
            return Response({"error": "Provide patient_id or patient_name"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(tags=['Reports'])
    def delete(self, request):
        patient_id = request.query_params.get('patient_id')
        patient_name = request.query_params.get('patient_name')

        if patient_id:
            report = get_object_or_404(Report, patient__patient_id=patient_id)
        elif patient_name:
            report = get_object_or_404(Report, patient__name__icontains=patient_name)
        else:
            return Response({"error": "Provide patient_id or patient_name"}, status=status.HTTP_400_BAD_REQUEST)

        report.delete()
        return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ReportByDoctor(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    doctor_param = openapi.Parameter(
        'doctor_name', openapi.IN_QUERY,
        description="Doctor's username to filter patient reports",
        type=openapi.TYPE_STRING,
        required=True
    )

    @swagger_auto_schema(manual_parameters=[doctor_param], tags=['Reports'])
    def get(self, request):
        doctor_name = request.query_params.get('doctor_name')
        if not doctor_name:
            return Response({"error": "Please provide a doctor_name"}, status=status.HTTP_400_BAD_REQUEST)

        reports = Report.objects.filter(doctor__user__username__icontains=doctor_name)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[doctor_param], tags=['Reports'])
    def put(self, request):
        doctor_name = request.query_params.get('doctor_name')
        if not doctor_name:
            return Response({"error": "Please provide a doctor_name"}, status=status.HTTP_400_BAD_REQUEST)

        report = get_object_or_404(Report, doctor__user__username__icontains=doctor_name)
        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[doctor_param], tags=['Reports'])
    def delete(self, request):
        doctor_name = request.query_params.get('doctor_name')
        if not doctor_name:
            return Response({"error": "Please provide a doctor_name"}, status=status.HTTP_400_BAD_REQUEST)

        report = get_object_or_404(Report, doctor__user__username__icontains=doctor_name)
        report.delete()
        return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    