from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    medical_history = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
