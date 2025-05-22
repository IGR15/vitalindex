from django.db import models
from users.models import User
from medical_records.models import MedicalRecord

class Student(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='education_students')
    academic_course = models.CharField(max_length=255)
    academic_year = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.academic_course}"

#GF
class CaseStudy(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['medical_record']
        
class SavedCaseStudy(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'case_study')


        