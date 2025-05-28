from django.urls import path
from reports.api.views import (
    CreateReport, ReportList, ReportDetail,
    ReportByPatient, ReportByDoctor,
    PublicReportsView, ReviewedReportsView
)

urlpatterns = [
    path('reports/', ReportList.as_view(), name='report-list'),
    path('reports/create/', CreateReport.as_view(), name='create-report'),
    path('reports/<int:report_id>/', ReportDetail.as_view(), name='report-detail'),
    
    path('reports/patient/', ReportByPatient.as_view(), name='report-by-patient'),
    path('reports/doctor/', ReportByDoctor.as_view(), name='report-by-doctor'),

    path('reports/public/', PublicReportsView.as_view(), name='public-reports'),
    path('reports/reviewed/', ReviewedReportsView.as_view(), name='reviewed-reports'),
]
