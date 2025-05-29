from django.db import models
from users.models import User
from medical_records.models import MedicalRecord

class SavedCaseStudy(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'medical_record')