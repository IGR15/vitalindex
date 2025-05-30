from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from patients.models import Patient
from users.permissions import IsAdminOrDoctor, IsAdminOrDoctorOrNurse
from rest_framework.permissions import IsAuthenticated
from education.models import SavedCaseStudy
from medical_records.models import MedicalRecord, Vital
from medical_records.api.serializers import (
    MedicalRecordSerializer,
    VitalsCreateSerializer,
    VitalsInlineSerializer,
    MedicalRecordUpdateSerializer
)
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class MedicalRecordByPatient(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, patient_id):
        try:
            patient = get_object_or_404(Patient, id=patient_id)
            medical_records = MedicalRecord.objects.filter(patient=patient).select_related('patient')

            serializer = MedicalRecordSerializer(medical_records, many=True, context={'request': request})
            return Response({
                "patient": {
                    "id": patient.id,
                    "first_name": patient.first_name,
                    "last_name": patient.last_name,
                    "dob": patient.date_of_birth,
                },
                "medical_records": serializer.data
            })
        except Exception as e:
            logger.exception(f"Unexpected error during MedicalRecordByPatient GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllMedicalRecords(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request):
        try:
            medical_records = MedicalRecord.objects.all().select_related('patient')

            if not medical_records.exists():
                return Response({"error": "No medical records found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = MedicalRecordSerializer(medical_records, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"Unexpected error during GetAllMedicalRecords GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedicalRecordByPatientName(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, patient_name):
        try:
            patients = Patient.objects.filter(
                Q(first_name__icontains=patient_name) | Q(last_name__icontains=patient_name)
            )

            if not patients.exists():
                return Response({"error": "No patients found with the given name"}, status=status.HTTP_404_NOT_FOUND)

            all_records = MedicalRecord.objects.filter(patient__in=patients).select_related('patient')

            if not all_records.exists():
                return Response({"error": f"No medical records found for patients matching '{patient_name}'"}, status=status.HTTP_404_NOT_FOUND)

            serializer = MedicalRecordSerializer(all_records, many=True, context={'request': request})
            return Response({
                "matches": patients.count(),
                "medical_records": serializer.data
            })
        except Exception as e:
            logger.exception(f"Unexpected error during MedicalRecordByPatientName GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateMedicalRecord(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(request_body=MedicalRecordSerializer, tags=['medical_records'])
    def post(self, request):
        try:
            data = request.data.copy()
            data.pop('patient', None)

            patient_id = data.get('patient_id')
            if not patient_id:
                return Response({"detail": "patient_id is required."}, status=status.HTTP_400_BAD_REQUEST)

            if not Patient.objects.filter(pk=patient_id).exists():
                return Response({"detail": "Patient does not exist."}, status=status.HTTP_404_NOT_FOUND)

            serializer = MedicalRecordSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Unexpected error during CreateMedicalRecord POST: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateVitals(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(request_body=VitalsCreateSerializer, tags=['vitals'])
    def post(self, request):
        try:
            medical_record_id = request.data.get("medical_record_id")

            if not medical_record_id:
                return Response({"error": "medical_record_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            medical_record = get_object_or_404(MedicalRecord, record_id=medical_record_id)

            data = request.data.copy()
            data["record"] = medical_record.record_id
            serializer = VitalsCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Unexpected error during CreateVitals POST: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedicalRecordDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, record_id):
        try:
            medical_record = get_object_or_404(MedicalRecord, record_id=record_id)
            serializer = MedicalRecordSerializer(medical_record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Unexpected error during MedicalRecordDetail GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=MedicalRecordUpdateSerializer, tags=['medical_records'])
    def put(self, request, record_id):
        try:
            medical_record = get_object_or_404(MedicalRecord, record_id=record_id)
            serializer = MedicalRecordUpdateSerializer(medical_record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Unexpected error during MedicalRecordDetail PUT: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['medical_records'])
    def delete(self, request, record_id):
        try:
            medical_record = get_object_or_404(MedicalRecord, record_id=record_id)
            medical_record.delete()
            return Response({"message": "Medical record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception(f"Unexpected error during MedicalRecordDetail DELETE: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(request_body=MedicalRecordSerializer, tags=['medical_records'])
    def put(self, request, pk):
        try:
            record = get_object_or_404(MedicalRecord, record_id=pk)
            serializer = MedicalRecordSerializer(record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Unexpected error during UpdateMedicalRecordView PUT: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VitalsDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['vitals'])
    def get(self, request, pk):
        try:
            vitals = get_object_or_404(Vital, pk=pk)
            serializer = VitalsCreateSerializer(vitals)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Unexpected error during VitalsDetail GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=VitalsInlineSerializer, tags=['vitals'])
    def put(self, request, pk):
        try:
            vitals = get_object_or_404(Vital, pk=pk)
            serializer = VitalsInlineSerializer(vitals, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Unexpected error during VitalsDetail PUT: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['vitals'])
    def delete(self, request, pk):
        try:
            vitals = get_object_or_404(Vital, pk=pk)
            vitals.delete()
            return Response({"message": "Vitals deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception(f"Unexpected error during VitalsDetail DELETE: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
