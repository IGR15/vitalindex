from django.urls import path
from education.api.views import (
   SaveCaseStudyView,MyCaseStudiesView
)

urlpatterns = [
    path('case-studies/save/', SaveCaseStudyView.as_view(), name='save-case-study'),
    path('case-studies/my/', MyCaseStudiesView.as_view(), name='my-case-studies'),
    path('case-studies/my/<int:record_id>/', MyCaseStudiesView.as_view(), name='delete-case-study'),
]
