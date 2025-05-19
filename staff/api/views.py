from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from users.permissions import IsDoctor,IsNurse,IsStudent
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail
import string
from rest_framework.response import Response
from staff.models import (Doctor,
                          Nurse,
                          Department,
                          Student,)
from users.models import User
import secrets
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from staff.api.serializers import (DoctorSerializer,
                                   NurseSerializer,
                                   StudentSerializer,
                                   DepartmentSerializer,)

# class CreateDoctor(APIView):
#     permission_classes = [IsAuthenticated] 
#     permission_classes = [IsAdminUser]
#     @swagger_auto_schema(request_body=DoctorSerializer, tags=['create doctor,nurse,student,'])
#     def post(self, request):
#         serializer = DoctorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateDoctor(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        request_body=DoctorSerializer,
        tags=['create doctor']
    )
    def post(self, request):
        data = request.data.copy()

        # Set password
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        data['user']["role"] = "Doctor"
        data['user']["password"] = password  # Inject password into serializer

        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            doctor = serializer.save()
            doctor.user.set_password(password)
            doctor.user.save()

            send_mail(
                subject="Your VitalIndex Login Credentials",
                message=f"Username: {doctor.user.username}\nPassword: {password}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor.user.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateNurse(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(request_body=NurseSerializer, tags=['create doctor,nurse,student,'])
    def post(self, request):
        data = request.data.copy()

        # Set password
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        data['user']["role"] = "Nurse"
        data['user']["password"] = password  # Inject password into serializer

        serializer = NurseSerializer(data=data)
        if serializer.is_valid():
            nurse = serializer.save()
            nurse.user.set_password(password)
            nurse.user.save()

            send_mail(
                subject="Your VitalIndex Login Credentials",
                message=f"Username: {nurse.user.username}\nPassword: {password}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[nurse.user.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateStudent(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(request_body=StudentSerializer,tags=['create doctor,nurse,student,'])
    def post(self, request):
        data = request.data.copy()

        # Set password
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        data['user']["role"] = "Student"
        data['user']["password"] = password  # Inject password into serializer

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            nurse = serializer.save()
            nurse.user.set_password(password)
            nurse.user.save()

            send_mail(
                subject="Your VitalIndex Login Credentials",
                message=f"Username: {nurse.user.username}\nPassword: {password}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[nurse.user.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateDepartment(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(request_body=DepartmentSerializer,tags=['create doctor,nurse,student,'])
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class DoctorList(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser,IsDoctor]
    @swagger_auto_schema(tags=['doctor'])
    def get(self, request):
        try:
            
            doctors = Doctor.objects.all()
        except Doctor.DoesNotExist:
            return Response({"error": "Doctors not found"}, status=status.HTTP_404_NOT_FOUND)    
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DoctorDetail(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser,IsDoctor]
    @swagger_auto_schema(tags=['doctor'])
    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)    
        
    @swagger_auto_schema(request_body=DoctorSerializer,tags=['doctor'])
    def put(self,request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor, data=request.data)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(tags=['doctor'])
    def delete(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            doctor.delete()
            return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
class NurseList(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser, IsDoctor]
    
    @swagger_auto_schema(tags=['nurse'])
    def get(self, request):
        try:
            nurses = Nurse.objects.all()
        except Nurse.DoesNotExist:
            return Response({"error": "Nurses not found"}, status=status.HTTP_404_NOT_FOUND)    
        serializer = NurseSerializer(nurses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NurseDetail(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser, IsDoctor]
    @swagger_auto_schema(tags=['nurse'])
    def get(self, request, pk):
        try:
            nurse = Nurse.objects.get(pk=pk)
            serializer = NurseSerializer(nurse)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Nurse.DoesNotExist:
            return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(request_body=NurseSerializer,tags=['nurse'])
    def put(self,request,pk):
        try:
            nurse = Nurse.objects.get(pk=pk)
            serializer = NurseSerializer(nurse, data=request.data)
        except Nurse.DoesNotExist:
            return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(tags=['nurse'])
    def delete(self, request, pk):
        try:
            nurse = Nurse.objects.get(pk=pk)
            nurse.delete()
            return Response({"message": "Nurse deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Nurse.DoesNotExist:
            return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class StudentList(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser, IsDoctor]
    @swagger_auto_schema(tags=['student'])
    def get(self, request):
        try:
            students = Student.objects.all()
        except Student.DoesNotExist:
            return Response({"error": "Students not found"}, status=status.HTTP_404_NOT_FOUND)    
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StudentDetail(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser, IsDoctor]
    @swagger_auto_schema(tags=['student'])
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(request_body=StudentSerializer,tags=['student'])
    def put(self,request,pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
    @swagger_auto_schema(tags=['student'])
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
class DepartmentList(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser, IsDoctor]
    @swagger_auto_schema(tags=['department'])
    def get(self, request):
        try:
            departments = Department.objects.all()
        except Department.DoesNotExist:
            return Response({"error": "Departments not found"}, status=status.HTTP_404_NOT_FOUND)    
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   
    
class DepartmentDetail(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser, IsDoctor]
    @swagger_auto_schema(tags=['department'])
    def get(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=DepartmentSerializer,tags=['department'])
    def put(self,request,pk):
        try:
            department = Department.objects.get(pk=pk)
            serializer = DepartmentSerializer(department, data=request.data)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['department'])
    def delete(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            department.delete()
            return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)