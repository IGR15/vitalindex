from django.db import models
from patients.models import Patient

class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_records")
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    observations = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"Record for {self.patient.name} - {self.created_date}"

class Vital(models.Model):  
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="vitals")
    temperature = models.FloatField()
    heart_rate = models.IntegerField()
    blood_pressure = models.CharField(max_length=20)
    oxygen_saturation = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.medical_record.patient.name} at {self.timestamp}"

