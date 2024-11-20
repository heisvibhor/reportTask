import uuid

from celery.result import AsyncResult
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .celery import generate_html_report_task, generate_pdf_report_task
from .models import Reports
from .serializer import EventsCollectionSerializer, ReportSerializer


@api_view(['POST'])
def generate_html_report(request):
    """
    Generate html report from the events return task id, can callback to get the report at /assignment/html/<task_id>
    :param request:
    :return: task_id
    """
    event = EventsCollectionSerializer(data=request.data)
    if not event.is_valid():
        return Response(event.errors, status=status.HTTP_400_BAD_REQUEST)

    task_id = generate_html_report_task.delay(request.data).id
    return Response({'task_id': task_id}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def check_task_and_get_html_report(request, id: uuid.uuid4):
    """
    Checks the status of the task and returns the html report if the task is completed
    """
    task = AsyncResult(str(id))
    response = {
        'task_id': id,
        'status': task.state,
        'data': None,
    }
    if task.state == 'SUCCESS':
        report = Reports.objects.filter(task_id=id)
        if report.exists():
            data = ReportSerializer(report.first()).data
            response['data'] = data
            response['message'] = 'Task completed'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['message'] = 'Task completed but report not found try again'
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    response['message'] = 'Task not complete or not found'
    return Response(response, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def generate_pdf_report(request):
    """
    Generate pdf report from the events return task id, can callback to get the report at /assignment/pdf/<task_id>
        :param request:
        :return: task_id
    """
    event = EventsCollectionSerializer(data=request.data)
    if not event.is_valid():
        return Response(event.errors, status=status.HTTP_400_BAD_REQUEST)

    task_id = generate_pdf_report_task.delay(request.data).id
    return Response({'task_id': task_id}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def check_task_and_get_pdf_report(request, id: uuid.uuid4):
    """
    Checks the status of the task and returns the html report if the task is completed
    """
    task = AsyncResult(str(id))
    response = {
        'task_id': id,
        'status': task.state,
    }

    report = Reports.objects.filter(task_id=id)
    if task.state == 'SUCCESS' or report.exists():
        if report.exists() and report.first().report_url:
            file = open(report.first().report_url, 'rb').read()
            response = HttpResponse(file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response
        else:
            response['message'] = 'Task completed but report not found try again'
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    response['message'] = 'Task not complete or not found'
    return Response(response, status=status.HTTP_202_ACCEPTED)