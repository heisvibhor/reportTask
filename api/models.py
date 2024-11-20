import uuid

from django.db import models
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportTask.settings')
# Create your models here.
class Reports(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    task_id = models.UUIDField()
    report = models.TextField()
    report_url = models.URLField()
    student_id = models.UUIDField()

    class Meta:
        indexes=[
            models.Index(fields=['task_id'])
        ]