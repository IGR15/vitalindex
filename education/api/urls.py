from django.urls import path
from education.api.views import (
    SaveCaseStudyView,
    SaveStudentCaseStudyView,
    MyBookmarkedCaseStudiesView,
    StudentCaseStudyView
)

urlpatterns = [
    path("publish/", SaveCaseStudyView.as_view(), name="publish_case_study"),
    path("student/save/", SaveStudentCaseStudyView.as_view(), name="save_student_case_study"),
    path("student/my/", MyBookmarkedCaseStudiesView.as_view(), name="my_bookmarked_case_studies"),
    path("student/case-study", StudentCaseStudyView.as_view,name="case-studylist"),
]
