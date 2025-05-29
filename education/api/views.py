from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.permissions import IsAdminOrDoctor, IsAdminOrDoctorOrNurseOrStudent
from medical_records.models import MedicalRecord
from education.models import SavedCaseStudy
from education.api.serializers import RedactedMedicalRecordSerializer


class PublishMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'medical_record_id': openapi.Schema(type=openapi.TYPE_INTEGER)},
            required=['medical_record_id']
        ),
        tags=['education']
    )
    def post(self, request):
        record_id = request.data.get("medical_record_id")
        if not record_id:
            return Response({"detail": "Missing medical_record_id"}, status=status.HTTP_400_BAD_REQUEST)

        record = get_object_or_404(MedicalRecord, pk=record_id)

        if record.is_public:
            return Response({"detail": "Already public."}, status=status.HTTP_409_CONFLICT)

        record.is_public = True
        record.save()

        return Response({"detail": "Medical record published as public."}, status=status.HTTP_200_OK)


class PublicMedicalRecordsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(tags=['education'])
    def get(self, request):
        records = MedicalRecord.objects.filter(is_public=True)
        serializer = RedactedMedicalRecordSerializer(records, many=True)
        return Response(serializer.data)


class SaveStudentBookmarkView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'medical_record_id': openapi.Schema(type=openapi.TYPE_INTEGER)},
            required=['medical_record_id']
        ),
        tags=['education']
    )
    def post(self, request):
        record_id = request.data.get("medical_record_id")
        record = get_object_or_404(MedicalRecord, pk=record_id, is_public=True)

        obj, created = SavedCaseStudy.objects.get_or_create(student=request.user, medical_record=record)
        if not created:
            return Response({"detail": "Already saved."}, status=status.HTTP_409_CONFLICT)
        return Response({"detail": "Bookmarked."}, status=status.HTTP_201_CREATED)


class MyBookmarkedRecordsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurseOrStudent]

    @swagger_auto_schema(tags=['education'])
    def get(self, request):
        bookmarks = SavedCaseStudy.objects.filter(student=request.user).select_related('medical_record')
        records = [b.medical_record for b in bookmarks]
        serializer = RedactedMedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
