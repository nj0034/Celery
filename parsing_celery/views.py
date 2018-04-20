from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from celery.result import AsyncResult
from django_celery_results.models import *
from .tasks import *
from datetime import datetime
import requests


def update_state(celery_task_id):
    task_result = TaskResult.objects.get(task_id=celery_task_id)

    result_info = {
        "celery_task_id": celery_task_id,
        "end_datetime": task_result.date_done,
        "state": task_result.status,
        "error_message": task_result.result
    }

    return result_info


class UpdateParsingState(APIView):
    def post(self, request):
        celery_task_id_list = dict(request.data).get('celery_task_id_list')
        print(celery_task_id_list)

        complete_task_list = list()

        for celery_task_id in celery_task_id_list:
            if AsyncResult(celery_task_id).ready():
                result_info = update_state(celery_task_id)
                complete_task_list.append(result_info)

        print(complete_task_list)

        return Response(status=status.HTTP_200_OK, data={"complete_task_list": complete_task_list})


class StartParsing(APIView):
    def post(self, request):
        sailer_name_list = dict(request.data).get('sailer_name_list')

        start_task_list = list()

        for sailer_name in sailer_name_list:
            task = parsing(sailer_name)

            result_info = {
                "sailer_name": sailer_name,
                "celery_task_id": task.id,
                "start_datetime": datetime.now()
            }

            start_task_list.append(result_info)

        return Response(status=status.HTTP_200_OK, data={"start_task_list": start_task_list})


class TerminateParsing(APIView):
    def post(self, request):
        celery_task_id_list = dict(request.data).get('celery_task_id_list')

        terminate_task_list = list()

        for celery_task_id in celery_task_id_list:
            if not AsyncResult(celery_task_id).ready():
                AsyncResult(celery_task_id).revoke(terminate=True)

            result_info = update_state(celery_task_id)
            terminate_task_list.append(result_info)

        return Response(status=status.HTTP_200_OK, data={"terminate_task_list": terminate_task_list})
