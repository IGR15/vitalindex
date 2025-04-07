from django.db import models
from staff.models import Doctor
from patients.models import Patient
from medical_records.models import MedicalRecord

class Report(models.Model):
    REPORT_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    report_id = models.AutoField(primary_key=True) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reports")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reports")
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name="reports")
    report_title = models.CharField(max_length=255)
    report_content = models.TextField()
    report_file = models.FileField(upload_to='reports/', null=True, blank=True) 
    # status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='draft')  
    doctor_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Report {self.report_id} - {self.report_title} (Dr. {self.doctor.user.username})"
