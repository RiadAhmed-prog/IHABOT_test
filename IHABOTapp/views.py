from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import data_serializer
from .models import vitals_data
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['GET'])
def get(request):
    data = vitals_data.objects.all()
    serialize = data_serializer(data, many=True)
    return Response(serialize.data)


@api_view(['POST'])
def post(request):
    data = JSONParser().parse(request)
    # print(courseSerializer)
    data_ser = data_serializer(data=data)
    if data_ser.is_valid():
        data_ser.save()
        return Response(data_ser.data, status=status.HTTP_201_CREATED)

    return Response(data_ser.errors)
