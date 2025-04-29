from django.contrib import admin
from .models import MedicalRecord, Vital

class VitalInline(admin.TabularInline):
    model = Vital
    extra = 0

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'patient', 'created_date', 'last_updated')
    search_fields = ('patient__name',)
    list_filter = ('created_date',)
    inlines = [VitalInline]
