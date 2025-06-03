from django.db import migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # No dependencies, first migration in 'core'
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            reverse_sql="DROP EXTENSION IF EXISTS pg_trgm;"
        )
    ]
