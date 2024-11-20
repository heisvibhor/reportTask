from django.urls import path

from .views import generate_html_report, check_task_and_get_html_report, generate_pdf_report, \
    check_task_and_get_pdf_report

urlpatterns = [
    path('assignment/html', generate_html_report, name='generate html report'),
    path('assignment/html/<uuid:id>', check_task_and_get_html_report, name='check task status and get html report'),
    path('assignment/pdf', generate_pdf_report, name='generate pdf report'),
    path('assignment/pdf/<uuid:id>', check_task_and_get_pdf_report, name='check task status and get pdf report')
]
