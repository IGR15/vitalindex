from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.permissions import IsDoctor,IsNurse,IsStudent
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from education.api.serializers import StudentSerializer
from education.models import Student, CaseStudy
from medical_records.models import MedicalRecord
from medical_records.api.serializers import RedactedMedicalRecordSerializer
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['education']))
class SaveCaseStudyView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        try:
            record_id = request.data.get("medical_record_id")
            if not record_id:
                return Response({"detail": "Missing medical_record_id"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                record = MedicalRecord.objects.get(pk=record_id)
            except MedicalRecord.DoesNotExist:
                return Response({"detail": "Medical record not found"}, status=status.HTTP_404_NOT_FOUND)

            if not record.is_public:
                return Response({"detail": "This medical record is not available for case study."}, status=status.HTTP_403_FORBIDDEN)

           
            if CaseStudy.objects.filter(student=request.user, medical_record=record).exists():
                return Response({"detail": "Already saved as case study."}, status=status.HTTP_409_CONFLICT)

            CaseStudy.objects.create(student=request.user, medical_record=record)
            return Response({"detail": "Case study saved successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['education']))
@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['education']))
class MyCaseStudiesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        try:
            case_studies = CaseStudy.objects.filter(student=request.user)
            medical_records = [cs.medical_record for cs in case_studies]

            if not medical_records:
                return Response({"detail": "No saved case studies."}, status=status.HTTP_404_NOT_FOUND)

            serializer = RedactedMedicalRecordSerializer(medical_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": f"Error retrieving case studies: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        
    def delete(self, request, record_id):
        try:
            try:
                record = MedicalRecord.objects.get(pk=record_id)
            except MedicalRecord.DoesNotExist:
                return Response({"detail": "Medical record not found."}, status=status.HTTP_404_NOT_FOUND)

            try:
                case_study = CaseStudy.objects.get(student=request.user, medical_record=record)
            except CaseStudy.DoesNotExist:
                return Response({"detail": "Case study not found in your saved list."}, status=status.HTTP_404_NOT_FOUND)

            case_study.delete()
            return Response({"detail": "Case study removed successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    