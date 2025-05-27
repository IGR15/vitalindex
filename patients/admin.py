from django.contrib import admin
from django import forms
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_of_birth', 'gender')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('gender',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'] = forms.CharField()
        return form

    def save_model(self, request, obj, form, change):
        full_name = form.cleaned_data.get('name')
        if full_name:
            obj.name = full_name  # uses @name.setter from your model
        super().save_model(request, obj, form, change)
#gpt