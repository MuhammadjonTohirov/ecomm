from datetime import datetime

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token
from rest_framework.serializers import Serializer
from rest_framework.utils import json

from helpers.defaults import CrmDefaults
from helpers.responses import AppResponse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from crm.models import Profile, Bank, Address, User, Organization, File
from crm.serializers import ProfileSerializer, BankSerializer, OrganizationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def init_default(request):
    message = 'Successfully created'
    is_banks_created = CrmDefaults.init_banks(request)
    message = message if is_banks_created else 'Error while creating'
    return Response(AppResponse(message, is_error=not is_banks_created).success_body())


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        User.objects.create_user(username=username, password=password, email=email).save()
        return Response(AppResponse(message='User has been created').success_body())
    except Exception as ex:
        return Response(AppResponse(message=ex.__str__()).unknown_error_body())


class BankViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    @action(methods=['GET'], detail=False)
    def get(self, request, pk=None):
        s = self.serializer_class(self.queryset, many=True)
        return Response(AppResponse(s.data).success_body())


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
        return Response(AppResponse(s.data).success_body())

    @action(methods=['POST'], detail=False)
    def add(self, request, pk=None):
        return Response()


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny, ]
    queryset = Profile.objects.all()

    @action(methods=['GET'], detail=False)
    def get(self, request, pk=None):
        user = request.user
        if user.id is None:
            return Response(AppResponse(message='No such user').unknown_error_body())
        try:
            profile = self.queryset.get(user=user)

            fn = profile.user.first_name
            ln = profile.user.last_name
            r = {
                'first_name': fn,
                'last_name': ln
            }

            return Response(AppResponse(r).success_body())
        except Exception as ex:
            print(ex.__str__())
            return Response(AppResponse(message='Need to fill profile').unknown_error_body())

    @action(methods=['POST'], detail=False)
    def add(self, request, pk=None):
        pass
