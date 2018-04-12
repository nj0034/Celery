from django.urls import path
from parsing_celery import views

app_name = 'parsing_celery'

urlpatterns = [
    path('', views.UpdateParsingState)
]