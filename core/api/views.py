from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from reports.models import Report
from patients.models import Patient
from .serializers import (
    ReportSearchSerializer,
    PatientSearchSerializer
)

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Global search across Reports and Patients. Pass query string as 'q' parameter.",
        manual_parameters=[
            openapi.Parameter(
                'q', openapi.IN_QUERY,
                description="Search query string",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'reports': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'report_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'report_title': openapi.Schema(type=openapi.TYPE_STRING),
                                'similarity': openapi.Schema(type=openapi.TYPE_NUMBER, format='float')
                            }
                        )
                    ),
                    'patients': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'patient_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'similarity': openapi.Schema(type=openapi.TYPE_NUMBER, format='float')
                            }
                        )
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        },
        tags=['Search']
    )
    def get(self, request):
        query = request.GET.get('q', '').strip()

        if not query:
            return Response({"detail": "Missing query param 'q'."}, status=400)

        # --- Search Reports ---
        report_results = Report.objects.annotate(
            similarity=TrigramSimilarity('report_content', query)
        ).filter(similarity__gt=0.3).order_by('-similarity')[:10]

        report_data = ReportSearchSerializer(report_results, many=True).data

        # --- Search Patients ---
        patient_results = Patient.objects.annotate(
            similarity=TrigramSimilarity('first_name', query)
        ).filter(similarity__gt=0.3).order_by('-similarity')[:10]

        patient_data = PatientSearchSerializer(patient_results, many=True).data

        # --- Assemble Response ---
        data = {
            "reports": report_data,
            "patients": patient_data
        }

        return Response(data)
