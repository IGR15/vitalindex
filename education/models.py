from django.db import models
from users.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    academic_course = models.CharField(max_length=255)
    academic_year = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.academic_course}"
