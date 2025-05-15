from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from users.permissions import IsDoctor, IsNurse, IsStudent
from staff.models import Doctor, Nurse, Department, Student
from staff.api.serializers import DoctorSerializer, NurseSerializer, StudentSerializer, DepartmentSerializer


# ----- CREATE VIEWS -----

@method_decorator(name='post', decorator=swagger_auto_schema(request_body=DoctorSerializer, responses={201: DoctorSerializer}))
class CreateDoctor(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='post', decorator=swagger_auto_schema(request_body=NurseSerializer, responses={201: NurseSerializer}))
class CreateNurse(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = NurseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='post', decorator=swagger_auto_schema(request_body=StudentSerializer, responses={201: StudentSerializer}))
class CreateStudent(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name='post', decorator=swagger_auto_schema(request_body=DepartmentSerializer, responses={201: DepartmentSerializer}))
class CreateDepartment(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----- LIST & DETAIL VIEWS -----

@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: DoctorSerializer(many=True)}))
class DoctorList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: DoctorSerializer, 404: 'Doctor not found'}))
@method_decorator(name='put', decorator=swagger_auto_schema(request_body=DoctorSerializer, responses={200: DoctorSerializer, 400: 'Bad Request', 404: 'Doctor not found'}))
@method_decorator(name='delete', decorator=swagger_auto_schema(responses={204: 'Doctor deleted successfully', 404: 'Doctor not found'}))
class DoctorDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            serializer = DoctorSerializer(doctor, data=request.data)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
            doctor.delete()
            return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: NurseSerializer(many=True)}))
class NurseList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request):
        nurses = Nurse.objects.all()
        serializer = NurseSerializer(nurses, many=True)
        return Response(serializer.data)


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: NurseSerializer, 404: 'Nurse not found'}))
@method_decorator(name='put', decorator=swagger_auto_schema(request_body=NurseSerializer, responses={200: NurseSerializer, 400: 'Bad Request', 404: 'Nurse not found'}))
@method_decorator(name='delete', decorator=swagger_auto_schema(responses={204: 'Nurse deleted successfully', 404: 'Nurse not found'}))
class NurseDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request, pk):
        try:
            nurse = Nurse.objects.get(pk=pk)
            serializer = NurseSerializer(nurse)
            return Response(serializer.data)
        except Nurse.DoesNotExist:
            return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            nurse = Nurse.objects.get(pk=pk)
            serializer = NurseSerializer(nurse, data=request.data)
        except Nurse.DoesNotExist:
            return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            nurse = Nurse.objects.get(pk=pk)
            nurse.delete()
            return Response({"message": "Nurse deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Nurse.DoesNotExist:
            return Response({"error": "Nurse not found"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: StudentSerializer(many=True)}))
class StudentList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: StudentSerializer, 404: 'Student not found'}))
@method_decorator(name='put', decorator=swagger_auto_schema(request_body=StudentSerializer, responses={200: StudentSerializer, 400: 'Bad Request', 404: 'Student not found'}))
@method_decorator(name='delete', decorator=swagger_auto_schema(responses={204: 'Student deleted successfully', 404: 'Student not found'}))
class StudentDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: DepartmentSerializer(many=True)}))
class DepartmentList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: DepartmentSerializer, 404: 'Department not found'}))
@method_decorator(name='put', decorator=swagger_auto_schema(request_body=DepartmentSerializer, responses={200: DepartmentSerializer, 400: 'Bad Request', 404: 'Department not found'}))
@method_decorator(name='delete', decorator=swagger_auto_schema(responses={204: 'Department deleted successfully', 404: 'Department not found'}))
class DepartmentDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, IsDoctor]

    def get(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            serializer = DepartmentSerializer(department, data=request.data)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            department.delete()
            return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
