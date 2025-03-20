import asyncio
from unittest import async_case
from django.shortcuts import render
from crm.helpers.organization_employee_helper import OrganizationEmployeeHelper
from crm.models.models import OrganizationAddress
from helpers.methods import Methods

from helpers.responses import AppResponse
from utils.app_constants import ORGANIZATION_KEY, STOCK_ID_KEY
from wms.models.stock_product import MergedProductsInStock, StockInProduct

from .serializers import InventorySerializer, StockInProductSerializer, StockPointSerializer, StockPointDefaultSerializer
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models.stock_point import StockPoint3
from asgiref.sync import sync_to_async

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser

class Pagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'

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
    organization_id = request.GET.get(ORGANIZATION_KEY, None)
    stockpoints = StockPoint3.objects.filter(belongs_to=organization_id)
    serializer = StockPointDefaultSerializer(stockpoints, many=True)
    return Response(AppResponse(serializer.data).body())

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_inventory(request):
    def has_access_on_stock(stock: StockPoint3) -> bool:
        return OrganizationEmployeeHelper.works_in_organization(request.user, stock.belongs_to)
    
    def is_admin() -> bool:
        return request.user.is_superuser
    
    # StockInProduct
    stock_id = request.GET.get(STOCK_ID_KEY, None)
    search_text = request.GET.get('search', None)
    size = int(request.GET.get('size', 20))
    page = int(request.GET.get('page', 0))
    
    
    if not stock_id:
        return Response(AppResponse('Stock id is required').bad_request())
    
    stock = StockPoint3.objects.filter(id=stock_id).first()

    if not stock:
        return Response(AppResponse('Stock not found').not_found())
    
    if has_access_on_stock(stock) is False and is_admin() is False:
        return Response(AppResponse('Access denied').access_denied())
    
    stockpoints = MergedProductsInStock.objects.filter(stock_point__id=stock_id)
    
    if search_text is not None:
        stockpoints = stockpoints.filter(product__title__icontains=search_text)
    
    total_pages = int(stockpoints.count() / size)
    products = stockpoints[(page * size):((page + 1) * size)]
    serializer = InventorySerializer(products, many=True)
    data = {
        'products': serializer.data,
        'pages': total_pages,
        'size': size,
        'products_count': serializer.data.__len__()
    }
    return Response(AppResponse(data).body())

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def stock_product_transactions(request):
    product_id = request.GET.get('product_id', None)
    search = request.GET.get('search', None)
    size = int(request.GET.get('size', 20))
    page = int(request.GET.get('page', 0))
    
    if not product_id:
        return Response(AppResponse('Product id is required').bad_request())
    
    products = StockInProduct.objects.filter(product__id=product_id)
    if search is not None:
        products = products.filter(product__title__icontains=search)
    paginator = Pagination()
    total_pages = int(products.count() / size)
    
    serializer = StockInProductSerializer(products, many=True)
    result_page= paginator.paginate_queryset(serializer.data, request)
    result = {
        'products': result_page,
        'pages': total_pages,
        'size': size,
        'products_count': serializer.data.__len__()
    }
    
    return Response(AppResponse(result).body())