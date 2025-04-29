from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_of_birth', 'gender')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('gender',)
