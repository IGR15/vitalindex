# Generated by Django 5.0.14 on 2025-05-27 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_records', '0002_medicalrecord_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='record_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
