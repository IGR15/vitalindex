from django.urls import path
from staff.api.views import (
    CreateDoctor, CreateNurse, CreateStudent, CreateDepartment,
    DoctorList, DoctorDetail,
    NurseList, NurseDetail,
    StudentList, StudentDetail,
    DepartmentList, DepartmentDetail
)

urlpatterns = [
    path('doctors/', DoctorList.as_view(), name='doctor-list'),  
    path('doctors/create/', CreateDoctor.as_view(), name='create-doctor'),  
    path('doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'), 

    path('nurses/', NurseList.as_view(), name='nurse-list'),  
    path('nurses/create/', CreateNurse.as_view(), name='create-nurse'),
    path('nurses/<int:pk>/', NurseDetail.as_view(), name='nurse-detail'),  

    path('students/', StudentList.as_view(), name='student-list'),  
    path('students/create/', CreateStudent.as_view(), name='create-student'), 
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'), 

    path('departments/', DepartmentList.as_view(), name='department-list'),  
    path('departments/create/', CreateDepartment.as_view(), name='create-department'),  
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),  
]
