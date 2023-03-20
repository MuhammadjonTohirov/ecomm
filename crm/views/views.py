from datetime import datetime
from time import sleep

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
import jwt
from rest_framework.serializers import Serializer
from rest_framework.utils import json
from crm.models.organization import Organization
from crm.models.User import User

from helpers.defaults import CrmDefaults
from helpers.responses import AppResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from crm.models.models import AppConfig, Person, Bank, Address, File
from crm.serializers import AppConfigSerializer, BankSerializer, OrganizationSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def init_default(request):
    message = 'Successfully created'
    is_banks_created = CrmDefaults.init_banks(request)
    message = message if is_banks_created else 'Error while creating'
    return Response(AppResponse(message, is_error=not is_banks_created).body())


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        User.objects.create_user(
            username=username, password=password, email=email).save()
        return Response(AppResponse(message='User has been created').body())
    except Exception as ex:
        return Response(AppResponse(message=ex.__str__()).body())


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_config(request):
    last_config = AppConfig.objects.last()
    serializer = AppConfigSerializer(last_config)
    sleep(2)
    return Response(AppResponse(serializer.data).body())


class BankViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    @action(methods=['GET'], detail=False)
    def get(self, request, pk=None):
        s = self.serializer_class(self.queryset, many=True)
        return Response(AppResponse(s.data).body())


class FileViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny, ]
    queryset = File.objects.all()

    @action(methods=['POST'], detail=False)
    def add(self, request, pk=None):
        return Response()


class OrganizationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(methods=['GET'], detail=False)
    def all(self, request, pk=None):
        s = self.serializer_class(self.queryset, many=True)
        return Response(AppResponse(s.data).body())

    @action(methods=['POST'], detail=False)
    def add(self, request, pk=None):
        return Response()
