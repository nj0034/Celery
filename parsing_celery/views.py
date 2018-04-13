from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

import requests


class UpdateParsingState(APIView):
    def post(self, request):
        celery_task_id_list = dict(request.data).get('celery_task_id_list')
        print(celery_task_id_list)

        return Response(status=status.HTTP_200_OK)
