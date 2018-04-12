from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

import requests


class UpdateParsingState(APIView):
    def get(self):
        return Response(status=status.HTTP_200_OK)
