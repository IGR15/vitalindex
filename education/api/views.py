from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.permissions import IsAdminOrDoctorOrNurseOrStudent,IsAdminOrDoctor
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from education.models import  CaseStudy,SavedCaseStudy
from medical_records.models import MedicalRecord
from medical_records.api.serializers import RedactedMedicalRecordSerializer
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from drf_yasg import openapi


class SaveCaseStudyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]  

    @swagger_auto_schema(request_body=RedactedMedicalRecordSerializer, tags=['education'])
    def post(self, request):
        record_id = request.data.get("medical_record_id")
        if not record_id:
            return Response({"detail": "Missing medical_record_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = MedicalRecord.objects.get(pk=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"detail": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

        if not record.is_public:
            return Response({"detail": "Record must be marked public before saving as a case study."}, status=status.HTTP_400_BAD_REQUEST)

        obj, created = CaseStudy.objects.get_or_create(medical_record=record)

        if not created:
            return Response({"detail": "Already available as case study."}, status=status.HTTP_409_CONFLICT)

        return Response({"detail": "Case study published successfully."}, status=status.HTTP_201_CREATED)

class SaveStudentCaseStudyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'medical_record_id': openapi.Schema(type=openapi.TYPE_INTEGER)},
        required=['medical_record_id']
    ), tags=['education'])
    def post(self, request):
        record_id = request.data.get("medical_record_id")
        if not record_id:
            return Response({"detail": "Missing medical_record_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = MedicalRecord.objects.get(pk=record_id)
        except MedicalRecord.DoesNotExist:
            return Response({"detail": "Medical record not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            case_study = CaseStudy.objects.get(medical_record=record)
        except CaseStudy.DoesNotExist:
            return Response({"detail": "This record is not available as a case study."}, status=status.HTTP_400_BAD_REQUEST)

        # Save to student's bookmarks
        saved_obj, created = SavedCaseStudy.objects.get_or_create(
            student=request.user, case_study=case_study
        )

        if not created:
            return Response({"detail": "Already saved."}, status=status.HTTP_409_CONFLICT)

        return Response({"detail": "Case study bookmarked successfully."}, status=status.HTTP_201_CREATED)

        
class StudentCaseStudyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(tags=["education"])
    def get(self, request):
        studies = CaseStudy.objects.select_related("medical_record").all()
        serialized = RedactedMedicalRecordSerializer(
            [study.medical_record for study in studies], many=True
        )
        return Response(serialized.data)


class MyBookmarkedCaseStudiesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(tags=['education'])
    def get(self, request):
        saved_links = SavedCaseStudy.objects.filter(student=request.user).select_related('case_study__medical_record')
        records = [link.case_study.medical_record for link in saved_links]

        serializer = RedactedMedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
