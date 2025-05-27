from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from patients.models import Patient
from users.permissions import (IsAdminOrDoctorOrNurse, IsAdminOrDoctor)
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from patients.api.serializers import PatientSerializer
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from django.db.models import Q


class CreatePatient(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor] 

    @swagger_auto_schema(request_body=PatientSerializer, tags=['patient'])
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientList(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['patient'])
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class PatientDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['patient'])
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PatientSerializer, tags=['patient'])
    def put(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['patient'])
    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response({"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PatientDetailByName(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    patient_param = openapi.Parameter(
        'patient_name', openapi.IN_QUERY,
        description="Patient's name to filter patient",
        type=openapi.TYPE_STRING,
        required=True
    )

    @swagger_auto_schema(manual_parameters=[patient_param], tags=['patient'])
    def get(self, request, pk=None):
        patient_name = request.query_params.get('patient_name')

        if pk:
            patient = get_object_or_404(Patient, pk=pk)
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif patient_name:
            patients = Patient.objects.filter(
             Q(first_name__icontains=patient_name) | Q(last_name__icontains=patient_name) |
             Q(first_name__icontains=patient_name.split()[0]) &
             Q(last_name__icontains=' '.join(patient_name.split()[1:]))
             #gpt
           )

            if not patients.exists():
                return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Provide either patient_id (pk) or patient_name"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PatientSerializer, manual_parameters=[patient_param], tags=['patient'])
    def put(self, request, pk=None):
        patient_name = request.query_params.get('patient_name')

        if pk:
            patient = get_object_or_404(Patient, pk=pk)
        elif patient_name:
            patient = get_object_or_404(Patient, name__icontains=patient_name)
        else:
            return Response({"error": "Provide either patient_id (pk) or patient_name"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[patient_param], tags=['patient'])
    def delete(self, request, pk=None):
        patient_name = request.query_params.get('patient_name')

        if pk:
            patient = get_object_or_404(Patient, pk=pk)
        elif patient_name:
            patient = get_object_or_404(Patient, name__icontains=patient_name)
        else:
            return Response({"error": "Provide either patient_id (pk) or patient_name"}, status=status.HTTP_400_BAD_REQUEST)

        patient.delete()
        return Response({"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
