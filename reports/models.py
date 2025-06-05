from django.db import models
from staff.models import Doctor
from patients.models import Patient
from medical_records.models import MedicalRecord
from users.models import User 

class Report(models.Model):
    REPORT_TYPES = [
        ('case_study', 'Case Study'),
        ('clinical_review', 'Clinical Review'),
        ('diagnostic_summary', 'Diagnostic Summary'),
        ('treatment_outcome', 'Treatment Outcome'),
    ]

    report_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reports")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reports")
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name="reports")

    report_title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=100, choices=REPORT_TYPES, default='case_study')
    report_content = models.TextField()
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    doctor_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)

    viewed_by = models.ManyToManyField(User, related_name="viewed_reports", blank=True)

    is_public = models.BooleanField(default=False, help_text="Mark if this report is shareable")

    keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    related_studies = models.TextField(blank=True, help_text="Links or references to studies")

    version = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.report_title} for {self.patient.first_name} ({self.report_type})"
