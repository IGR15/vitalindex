from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsAdminOrDoctor, IsAdminOrDoctorOrNurse
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail
import string
import secrets
from rest_framework.response import Response
from staff.models import Doctor, Nurse, Department, Student
from smtplib import SMTPException
from django.db import DatabaseError
from drf_yasg.utils import swagger_auto_schema
from staff.api.serializers import (
    DoctorSerializer, NurseSerializer, StudentSerializer, DepartmentSerializer,DoctorSerializerForPUT,NurseSerializerForPUT,StudentSerializerForPUT
)
from django.http import Http404
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)
from rest_framework.response import Response
from rest_framework import status

class CreateDoctor(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=DoctorSerializer, tags=['create doctor,nurse,student'])
    def post(self, request):
        try:
            data = request.data.copy()
            user_data = data.get('user')

            if not user_data or not isinstance(user_data, dict):
                return Response({"user": ["This field is required and must be an object."]}, status=status.HTTP_400_BAD_REQUEST)

            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user_data["role"] = "Doctor"
            user_data["password"] = password

            serializer = DoctorSerializer(data=data)
            if serializer.is_valid():
                doctor = serializer.save()
                doctor.user.set_password(password)
                doctor.user.save()

                try:
                    send_mail(
                        subject="Your VitalIndex Login Credentials",
                        message=f"Username: {doctor.user.username}\nPassword: {password}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[doctor.user.email],
                        fail_silently=False,
                    )
                except SMTPException as e:
                    logger.error(f"Failed to send email to {doctor.user.email}: {str(e)}")
                    return Response({"error": "Doctor created but failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as e:
            logger.error(f"Database error during doctor creation: {str(e)}")
            return Response({"error": "Internal database error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception(f"Unexpected error during doctor creation: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateNurse(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=NurseSerializer, tags=['create doctor,nurse,student'])
    def post(self, request):
        try:
            data = request.data.copy()
            user_data = data.get('user')

            if not user_data or not isinstance(user_data, dict):
                return Response({"user": ["This field is required and must be an object."]}, status=status.HTTP_400_BAD_REQUEST)

            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user_data["role"] = "Nurse"
            user_data["password"] = password

            serializer = NurseSerializer(data=data)
            if serializer.is_valid():
                nurse = serializer.save()
                nurse.user.set_password(password)
                nurse.user.save()

                try:
                    send_mail(
                        subject="Your VitalIndex Login Credentials",
                        message=f"Username: {nurse.user.username}\nPassword: {password}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[nurse.user.email],
                        fail_silently=False,
                    )
                except SMTPException as e:
                    logger.error(f"Failed to send email to {nurse.user.email}: {str(e)}")
                    return Response({"error": "Nurse created but failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as e:
            logger.error(f"Database error during nurse creation: {str(e)}")
            return Response({"error": "Internal database error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception(f"Unexpected error during nurse creation: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateStudent(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=StudentSerializer, tags=['create doctor,nurse,student'])
    def post(self, request):
        try:
            data = request.data.copy()
            user_data = data.get('user')

            if not user_data or not isinstance(user_data, dict):
                return Response({"user": ["This field is required and must be an object."]}, status=status.HTTP_400_BAD_REQUEST)

            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user_data["role"] = "Student"
            user_data["password"] = password

            serializer = StudentSerializer(data=data)
            if serializer.is_valid():
                student = serializer.save()
                student.user.set_password(password)
                student.user.save()

                try:
                    send_mail(
                        subject="Your VitalIndex Login Credentials",
                        message=f"Username: {student.user.username}\nPassword: {password}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[student.user.email],
                        fail_silently=False,
                    )
                except SMTPException as e:
                    logger.error(f"Failed to send email to {student.user.email}: {str(e)}")
                    return Response({"error": "Student created but failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as e:
            logger.error(f"Database error during student creation: {str(e)}")
            return Response({"error": "Internal database error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception(f"Unexpected error during student creation: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateDepartment(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=DepartmentSerializer, tags=['create doctor,nurse,student'])
    def post(self, request):
        try:
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DatabaseError as e:
            logger.error(f"Database error during department creation: {str(e)}")
            return Response({"error": "Internal database error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception(f"Unexpected error during department creation: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorList(APIView):
    permission_classes = [IsAdminOrDoctor]

    @swagger_auto_schema(tags=['doctor'])
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NurseList(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['nurse'])
    def get(self, request):
        nurses = Nurse.objects.all()
        serializer = NurseSerializer(nurses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentList(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['student'])
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DepartmentList(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['department'])
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['doctor'])
    def get(self, request, pk):
        try:
            doctor = get_object_or_404(Doctor, pk=pk)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Http404:
            return Response({
                "error": "Doctor not found",
                "message": f"No doctor was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during doctor GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=DoctorSerializerForPUT, tags=['doctor'])
    def put(self, request, pk):
        try:
            doctor = get_object_or_404(Doctor, pk=pk)
            serializer = DoctorSerializerForPUT(doctor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response({
                "error": "Doctor not found",
                "message": f"No doctor was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during doctor PUT: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['doctor'])
    def delete(self, request, pk):
        try:
            doctor = get_object_or_404(Doctor, pk=pk)
            doctor.delete()
            return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({
                "error": "Doctor not found",
                "message": f"No doctor was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during doctor DELETE: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NurseDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrNurse]

    @swagger_auto_schema(tags=['nurse'])
    def get(self, request, pk):
        try:
            nurse = get_object_or_404(Nurse, pk=pk)
            serializer = NurseSerializer(nurse)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Http404:
            return Response({
                "error": "Nurse not found",
                "message": f"No nurse was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during nurse GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=NurseSerializerForPUT, tags=['nurse'])
    def put(self, request, pk):
        try:
            nurse = get_object_or_404(Nurse, pk=pk)
            serializer = NurseSerializerForPUT(nurse, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response({
                "error": "Nurse not found",
                "message": f"No nurse was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during nurse PUT: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['nurse'])
    def delete(self, request, pk):
        try:
            nurse = get_object_or_404(Nurse, pk=pk)
            nurse.delete()
            return Response({"message": "Nurse deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({
                "error": "Nurse not found",
                "message": f"No nurse was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during nurse DELETE: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['student'])
    def get(self, request, pk):
        try:
            student = get_object_or_404(Student, pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Http404:
            return Response({
                "error": "Student not found",
                "message": f"No student was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during student GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=StudentSerializerForPUT, tags=['student'])
    def put(self, request, pk):
        try:
            student = get_object_or_404(Student, pk=pk)
            serializer = StudentSerializerForPUT(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response({
                "error": "Student not found",
                "message": f"No student was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during student PUT: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['student'])
    def delete(self, request, pk):
        try:
            student = get_object_or_404(Student, pk=pk)
            student.delete()
            return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({
                "error": "Student not found",
                "message": f"No student was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during student DELETE: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrDoctor]

    @swagger_auto_schema(tags=['department'])
    def get(self, request, pk):
        try:
            department = get_object_or_404(Department, pk=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Http404:
            return Response({
                "error": "Department not found",
                "message": f"No department was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during department GET: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=DepartmentSerializer, tags=['department'])
    def put(self, request, pk):
        try:
            department = get_object_or_404(Department, pk=pk)
            serializer = DepartmentSerializer(department, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response({
                "error": "Department not found",
                "message": f"No department was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during department PUT: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['department'])
    def delete(self, request, pk):
        try:
            department = get_object_or_404(Department, pk=pk)
            department.delete()
            return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response({
                "error": "Department not found",
                "message": f"No department was found with the provided ID ({pk}). Please verify and try again.",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Unexpected error during department DELETE: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
