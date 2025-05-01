from django.db import models
from users.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    doctor_id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    joining_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Dr. {self.user.name} - {self.specialization}"

class Nurse(models.Model):
    nurse_id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    assigned_shift = models.CharField(max_length=50)

    def __str__(self):
        return f"Nurse {self.user.name} - {self.assigned_shift}"


class Student(models.Model):
    student_id=models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='staff_students')
    academic_course = models.CharField(max_length=255)
    academic_year = models.IntegerField()
    
    def __str__(self):
        return f"Student {self.user.name}"
    
    
    