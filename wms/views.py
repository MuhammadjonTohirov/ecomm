import asyncio
from unittest import async_case
from django.shortcuts import render
from crm.models.models import OrganizationAddress
from helpers.methods import Methods

from helpers.responses import AppResponse

from .serializers import StockPointSerializer, StockPointDefaultSerializer
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models.stock_point import StockPoint3
from asgiref.sync import sync_to_async

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser


class StockPointView(viewsets.ViewSet):
    queryset = StockPoint3.objects.all()
    serializer_class = StockPointSerializer

    @action(methods=['GET'], detail=False)
    async def get(self, request, pk=None):

        latitude = float(request.GET.get('lat', None))
        longitude = float(request.GET.get('lng', None))
        _ids = []

        async for item in self.queryset:
            address: OrganizationAddress = item.address
            origin = address.latitude, address.longitude
            destination = latitude, longitude
            if Methods.is_in_range(origin, destination):
                print(Methods.distance(origin, destination))
                _ids.append(item.pk)

        s = self.serializer_class(StockPoint3.objects.filter(
            id__in=_ids), many=True, destination=destination)

        return Response(AppResponse(s.data).body())


@sync_to_async
def get_nearby_points(request):
    latitude = float(request.GET.get('lat', None))
    longitude = float(request.GET.get('lng', None))
    _ids = []

    for item in StockPoint3.objects.all():
        address: OrganizationAddress = item.address
        origin = address.latitude, address.longitude
        destination = latitude, longitude
        if Methods.is_in_range(origin, destination):
            print(Methods.distance(origin, destination))
            _ids.append(item.pk)

    s = StockPointSerializer(StockPoint3.objects.filter(
        id__in=_ids), many=True,
        destination=destination
    )

    return Response(AppResponse(s.data).body())


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_stockpoints(request):
    organization_id = request.GET.get('organization_id', None)
    stockpoints = StockPoint3.objects.filter(belongs_to=organization_id)
    serializer = StockPointDefaultSerializer(stockpoints, many=True)
    return Response(AppResponse(serializer.data).body())
