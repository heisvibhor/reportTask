# Generated by Django 5.1.3 on 2024-11-19 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='reports',
            index=models.Index(fields=['task_id'], name='api_reports_task_id_a6a3f1_idx'),
        ),
    ]
