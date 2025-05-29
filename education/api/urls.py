from django.urls import path
from .views import (
    PublishMedicalRecordView,
    PublicMedicalRecordsView,
    SaveStudentBookmarkView,
    MyBookmarkedRecordsView
)

urlpatterns = [
    path('education/publish/', PublishMedicalRecordView.as_view(), name='publish-medical-record'),
    path('education/public-records/', PublicMedicalRecordsView.as_view(), name='public-medical-records'),
    path('education/bookmark/', SaveStudentBookmarkView.as_view(), name='bookmark-medical-record'),
    path('education/my-bookmarks/', MyBookmarkedRecordsView.as_view(), name='my-bookmarked-records'),
]
