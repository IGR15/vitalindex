from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from staff.models import Doctor, Department
from patients.models import Patient
from reports.models import Report
from medical_records.models import MedicalRecord, Vital
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date


class MedicalRecordVitalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name='Cardiology')

        self.user = User.objects.create_user(
            username='docuser', password='password', email='doc@example.com', role='Doctor'
        )

        self.doctor = Doctor.objects.create(
            user=self.user,
            specialization="Cardiology",
            license_number="DOC123456",
            joining_date=date(2022, 5, 10),
            department=self.department
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.patient = Patient.objects.create(
            first_name='Ali',
            last_name='Zidan',
            date_of_birth='1990-01-01',
            gender='Male',
            address='Hebron',
            phone='1234567890',
            email='ali@example.com'
        )

        self.report = Report.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            report_title="Initial Report",
            report_type="case_study",
            report_content="Initial content"
        )

        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            diagnosis="Test Diagnosis",
            treatment_plan="Test Plan",
            observations="Test Observation",
            is_public=False
        )

    def test_create_medical_record(self):
        payload = {
            "patient_id": self.patient.id,
            "diagnosis": "New Diagnosis",
            "treatment_plan": "New Plan",
            "observations": "New Observations",
            "is_public": True
        }
        response = self.client.post(reverse('create-medical-record'), data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["diagnosis"], "New Diagnosis")

    def test_get_medical_record(self):
        url = reverse("medical-record-detail", args=[self.medical_record.record_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["diagnosis"], self.medical_record.diagnosis)

    def test_update_medical_record(self):
        url = reverse("medical-record-detail", args=[self.medical_record.record_id])
        payload = {
            "diagnosis": "Updated Diagnosis"
        }
        response = self.client.put(url, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["diagnosis"], "Updated Diagnosis")

    def test_delete_medical_record(self):
        url = reverse("medical-record-detail", args=[self.medical_record.record_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(MedicalRecord.objects.filter(record_id=self.medical_record.record_id).exists())

    def test_create_vitals(self):
        payload = {
            "medical_record_id": self.medical_record.record_id,
            "temperature": 37.5,
            "heart_rate": 75,
            "blood_pressure": "120/80",
            "oxygen_saturation": 98.0
        }
        response = self.client.post(reverse("create-vitals"), data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["heart_rate"], 75)
