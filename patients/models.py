from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False, default='First')
    last_name = models.CharField(max_length=100, null=False, blank=False, default='Last')

    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    medical_history = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @name.setter
    def name(self, value):
        parts = value.split()
        self.first_name = parts[0]
        self.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

