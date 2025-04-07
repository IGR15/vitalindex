from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from education.api.serializers import StudentSerializer
from education.models import Student


class CreateStudent(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    def get(self, request, pk):
        try:
            student = get_object_or_404(Student, pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            student = get_object_or_404(Student, pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            student = get_object_or_404(Student, pk=pk)
            student.delete()
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
class StudentList(APIView):
    def get(self, request):
        try:
            students = Student.objects.all()
        except Student.DoesNotExist:
            return Response({"error": "Students not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(students, many=True)  
        return Response(serializer.data)  