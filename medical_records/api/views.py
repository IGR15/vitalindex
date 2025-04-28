from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from patients.models import Patient
from users.permissions import IsDoctor,IsNurse,IsStudent
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from medical_records.models import MedicalRecord,Vitals
from medical_records.api.serializers import MedicalRecordSerializer,VitalsSerializer


class CreateMedicalRecord(APIView):
    permission_classes = [IsAuthenticated] 
    permission_classes = [IsAdminUser,IsDoctor,IsNurse]
    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateVitals(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser,IsDoctor,IsNurse]
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
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser,IsDoctor,IsNurse]
    def get(self, request, record_id):
        try: 
            medical_record = get_object_or_404(MedicalRecord, id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicalRecordSerializer(medical_record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    
    def delete(self, request, record_id):
        try:
            medical_record = get_object_or_404(MedicalRecord, id=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)
        medical_record.delete()
        return Response({"message": "Medical record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class VitalsDetail(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser,IsDoctor,IsNurse]
    def get(self, request, pk):
        try:
            vitals = get_object_or_404(Vitals, pk=pk)
        except Vitals.DoesNotExist:
            return Response({"error": "Vitals not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VitalsSerializer(vitals)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
    def put(self, request, pk):
        try:
            vitals = get_object_or_404(Vitals, pk=pk)
        except Vitals.DoesNotExist:
            return Response({"error": "Vitals not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VitalsSerializer(vitals, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            vitals = get_object_or_404(Vitals, pk=pk)
        except Vitals.DoesNotExist:
            return Response({"error": "Vitals not found"}, status=status.HTTP_404_NOT_FOUND)
        vitals.delete()
        return Response({"message": "Vitals deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class MedicalRecordsByPatientAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor, IsNurse]
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
