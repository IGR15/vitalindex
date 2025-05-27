from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from patients.models import Patient
from users.permissions import (IsAdminOrDoctor,IsAdminOrDoctorOrNurse,IsAdminOrDoctorOrNurseOrStudent)
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from medical_records.models import MedicalRecord,Vital
from education.models import CaseStudy
from medical_records.api.serializers import MedicalRecordSerializer,VitalsSerializer,RedactedMedicalRecordSerializer
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

class SingleEducationalRecordView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, pk):
        try:
            record = MedicalRecord.objects.get(pk=pk)
        except MedicalRecord.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if not record.is_public:
            return Response({"detail": "This record is not public."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RedactedMedicalRecordSerializer(record)
        return Response(serializer.data)

class EducationalRecordsView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request):
        try:
            records = MedicalRecord.objects.filter(is_public=True)
            if not records.exists():
                return Response(
                    {"detail": "No educational records found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = RedactedMedicalRecordSerializer(records, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"detail": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class MedicalRecordByPatient(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, patient_id):
        try:
            patient = get_object_or_404(Patient, id=patient_id)
            medical_records = MedicalRecord.objects.filter(patient=patient).select_related('patient')
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        if not medical_records.exists():
            return Response({"error": f"No medical records found for patient {patient.name}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicalRecordSerializer(medical_records, many=True)
        return Response({
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "dob": patient.dob,
            },
            "medical_records": serializer.data
        })
        
        
class medicalRecordByPatienName(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, patient_name):
        try:
            patient = get_object_or_404(Patient, name=patient_name)
            medical_records = MedicalRecord.objects.filter(patient=patient).select_related('patient')
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        if not medical_records.exists():
            return Response({"error": f"No medical records found for patient {patient.name}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicalRecordSerializer(medical_records, many=True)
        return Response({
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "dob": patient.dob,
            },
            "medical_records": serializer.data
        })

class CreateMedicalRecord(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(request_body=MedicalRecordSerializer, tags=['medical_records'])
    def post(self, request):
        
        data = request.data.copy()
        data.pop('patient', None) 

        patient_id = data.get('patient_id')
        if not patient_id:
            return Response({"detail": "patient_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate patient existence
        if not Patient.objects.filter(pk=patient_id).exists():
            return Response({"detail": "Patient does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicalRecordSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateVitals(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrDoctorOrNurse]
    @swagger_auto_schema(request_body=VitalsSerializer,tags=['vitals'])
    def post(self, request):
        medical_record_id = request.data.get("medical_record_id") 

        if not medical_record_id:
            return Response({"error": "medical_record_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        medical_record = get_object_or_404(MedicalRecord, id=medical_record_id) 
        
        request.data["record"] = medical_record.id  
        serializer = VitalsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MedicalRecordDetail(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrDoctorOrNurse]
    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, record_id):
        try: 
            medical_record = get_object_or_404(MedicalRecord, id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicalRecordSerializer(medical_record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=MedicalRecordSerializer,tags=['medical_records'])
    def put(self, request, record_id):
        try:
            medical_record = get_object_or_404(MedicalRecord, id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicalRecordSerializer(medical_record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(tags=['medical_records'])
    def delete(self, request, record_id):
        try:
            medical_record = get_object_or_404(MedicalRecord, id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)
        medical_record.delete()
        return Response({"message": "Medical record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class UpdateMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(request_body=MedicalRecordSerializer, tags=['medical_records'])
    def put(self, request, pk):
        try:
            record = MedicalRecord.objects.get(pk=pk)
        except MedicalRecord.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicalRecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            was_public = record.is_public
            serializer.save()

            # Auto-create CaseStudy if public is newly enabled
            if not was_public and serializer.validated_data.get("is_public", False):
                CaseStudy.objects.get_or_create(medical_record=record)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VitalsDetail(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrDoctorOrNurse]
    @swagger_auto_schema(tags=['vitals'])
    def get(self, request, pk):
        try:
            vitals = get_object_or_404(Vital, pk=pk)
        except Vital.DoesNotExist:
            return Response({"error": "Vitals not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VitalsSerializer(vitals)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    @swagger_auto_schema(request_body=VitalsSerializer,tags=['vitals'])
    def put(self, request, pk):
        try:
            vitals = get_object_or_404(Vital, pk=pk)
        except Vital.DoesNotExist:
            return Response({"error": "Vitals not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VitalsSerializer(vitals, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(tags=['vitals'])
    def delete(self, request, pk):
        try:
            vitals = get_object_or_404(Vital, pk=pk)
        except Vital.DoesNotExist:
            return Response({"error": "Vitals not found"}, status=status.HTTP_404_NOT_FOUND)
        vitals.delete()
        return Response({"message": "Vitals deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class MedicalRecordsByPatientAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]
    @swagger_auto_schema(tags=['medical_records'])
    def get(self, request, patient_id):
        try:
            patient = get_object_or_404(Patient, id=patient_id)
            medical_records = MedicalRecord.objects.filter(patient=patient).select_related('patient')
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        if not medical_records.exists():
            return Response({"error": f"No medical records found for patient {patient.name}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MedicalRecordSerializer(medical_records, many=True)
        return Response({
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "dob": patient.dob,
                "gender": patient.gender,
                "phone": patient.phone,
                "email": patient.email,
                "medical_history": patient.medical_history
            },
            "medical_records": serializer.data
        }, status=status.HTTP_200_OK)
