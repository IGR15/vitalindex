from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from patients.models import Patient
from staff.models import Doctor, Department
from reports.models import Report
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken
from notifications.models import Notification

# ✅ Add this:
from asgiref.testing import ApplicationCommunicator
from channels.layers import get_channel_layer

class ReportAPITest(TestCase):
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

        self.channel_layer = get_channel_layer()
        if self.channel_layer is None:
            from channels.layers import InMemoryChannelLayer
            self.channel_layer = InMemoryChannelLayer()
            import channels
            channels.layers.channel_layers = {"default": self.channel_layer}

    def test_create_report_success(self):
        payload = {
            "report_title": "Heart Case",
            "report_type": "case_study",
            "report_content": "Details...",
            "doctor_id": self.doctor.doctor_id,
            "patient_id": self.patient.id
        }
        response = self.client.post(reverse('create-report'), data=payload)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['report_title'], "Heart Case")

        notifications = Notification.objects.filter(user=self.user)
        self.assertTrue(notifications.exists(), "No notification created for doctor")
        latest_notification = notifications.latest('created_at')
        self.assertIn("New report published", latest_notification.content)  
        self.assertFalse(latest_notification.is_read)   

    def test_update_report_success(self):
        payload = {
            "report_title": "Updated Report Title",
            "report_content": "Updated content"
        }
        url = reverse('report-detail', args=[self.report.report_id])
        response = self.client.put(url, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['report_title'], "Updated Report Title")

    def test_doctor_cannot_update_unowned_report(self):
        other_user = User.objects.create_user(
            username='otherdoc', password='password', email='other@example.com', role='Doctor'
        )
        Doctor.objects.create(
            user=other_user,
            specialization="Neurology",
            license_number="DOC999999",
            joining_date=date(2023, 1, 1),
            department=self.department
        )
        refresh = RefreshToken.for_user(other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        payload = {"report_title": "Hacked"}
        url = reverse('report-detail', args=[self.report.report_id])
        response = self.client.put(url, data=payload)
        self.assertEqual(response.status_code, 403)

    def test_delete_report_success(self):
        url = reverse('report-detail', args=[self.report.report_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Report.objects.filter(report_id=self.report.report_id).exists())

    def test_doctor_cannot_delete_unowned_report(self):
        other_user = User.objects.create_user(
            username='otherdoc2', password='password', email='other2@example.com', role='Doctor'
        )
        Doctor.objects.create(
            user=other_user,
            specialization="Neurology",
            license_number="DOC888888",
            joining_date=date(2023, 1, 1),
            department=self.department
        )
        refresh = RefreshToken.for_user(other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('report-detail', args=[self.report.report_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_create_report_invalid_data(self):
        payload = {
            "report_title": "",  
            "report_type": "invalid_type",  
            "report_content": "Some content"
        }
        response = self.client.post(reverse('create-report'), data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('report_title', response.data)
        self.assertIn('report_type', response.data)
