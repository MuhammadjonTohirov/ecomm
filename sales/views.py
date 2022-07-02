from itertools import count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from helpers.responses import AppResponse
from sales.serializers import ProductCategorySerializer, ProductSerializer
from wms.models import ProductCategory, StockProduct
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

# Create your views here.

def index(request):
    return render(request, 'frontend/index/index.html')


def other(request):
    return HttpResponse(content='<h1>Other Page</h1>')

@api_view(['GET'])
@permission_classes([AllowAny, ])
def products(request):  
    product_category = request.GET.get('category', None)
    page = int(request.GET.get('page', 0))
    limit = int(request.GET.get('limit', 10))
    offset = page * limit
    # filter stockproduct by limit and page
    # stock_products = StockProduct.objects.filter(product_category=product_category).order_by('-id')[offset:offset+limit]

    if product_category is not None:
        products = StockProduct.objects.filter(product__categories=product_category).order_by('-id')[offset:offset+limit]
    else:
        products = StockProduct.objects.all().order_by('-id')[offset:offset+limit]
    serializer = ProductSerializer(products, many=True)
    return Response(AppResponse(serializer.data).body())


# create get categories
@api_view(['GET'])
@permission_classes([AllowAny, ])
def categories(request):
    categories = ProductCategory.objects.filter(parent = None)
    serializer = ProductCategorySerializer(categories, many=True)
    
    return Response(AppResponse(serializer.data).body())