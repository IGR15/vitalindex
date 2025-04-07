from django.urls import path
from education.api.views import (
    CreateStudent, StudentDetail, StudentList
)

urlpatterns = [
    path('students/', StudentList.as_view(), name='student-list'),  
    path('students/create/', CreateStudent.as_view(), name='create-student'), 
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'),  #
]
