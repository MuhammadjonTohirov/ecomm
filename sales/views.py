from itertools import count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from helpers.responses import AppResponse
from sales.serializers import ProductSerializer
from wms.models import ProductDetails, StockProduct
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
@permission_classes([IsAuthenticated, ])
def products(request):
    products = StockProduct.objects.filter(count__gt=0)
    serializer = ProductSerializer(products, many=True)
    return Response(AppResponse(serializer.data).success_body())