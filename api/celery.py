import os
import uuid
from time import sleep

from celery import Celery
from django.conf import settings
from xhtml2pdf import pisa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportTask.settings')

app = Celery('reportTask')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

def get_html_report(events_collection):
    events = events_collection.get('events')

    units_presence = set()
    for event in events:
        unit = event.get('unit')
        if unit:
            units_presence.add(int(unit))

    units = list(units_presence)
    units.sort()
    units_question_alias_map  = {unit: str(i+1) for i, unit in enumerate(units)}

    event_order = []
    for event in events:
        event_order.append('Q' + units_question_alias_map.get(int(event.get('unit'))))

    report = f'''<h2>Student ID: {events_collection.get("student_id")}</h2>
<p>Event Order: {' -> '.join(event_order)}</p>'''

    return report

@app.task(bind=True)
def generate_html_report_task(self, events_collection):
    report = get_html_report(events_collection)
    from .models import Reports
    Reports.objects.create(task_id=self.request.id, report=report, student_id=events_collection.get('student_id'))
    return 'Success'

@app.task(bind=True)
def generate_pdf_report_task(self, events_collection):
    report = get_html_report(events_collection)
    report_path = f'{settings.MEDIA_ROOT}/{uuid.uuid4()}.pdf'
    pdf_file = open(report_path, 'w+b')
    status = pisa.CreatePDF(report, dest=pdf_file)
    pdf_file.close()
    if status.err:
        raise Exception('Error while generating pdf', status.err)

    from .models import Reports
    Reports.objects.create(task_id=self.request.id, report=report, report_url=report_path, student_id=events_collection.get('student_id'))
    return 'Success'


app.register_task(generate_html_report_task)
app.register_task(generate_pdf_report_task)