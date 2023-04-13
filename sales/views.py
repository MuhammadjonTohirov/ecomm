from itertools import count
from time import sleep
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from crm.models.organization import Organization
from helpers.responses import AppResponse
from wms.models.stock_product import StockProduct
from .models.news import News
from sales.serializers import NewsSerializer, ProductCategorySerializer, ProductSerializer
from wms.models.product_category import ProductCategory
import wms.views as wms_views
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
import asyncio
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

def index(request):
    # get query parameters
    params = request.GET
    id = params.get('organization', None)
    if id is None:
        return HttpResponse(content='<h1>Organization is not specified</h1>')

    organization = Organization.objects.get(id=id)
    return render(request, 'frontend/index/index.html', context={'is_nav_sidebar_enabled': True, 'organization': organization})

def dashboard(request):
    # get query parameters
    return render(request, 'new/home/index.html')


def other(request):
    return HttpResponse(content='<h1>Other Page</h1>')

# create swagger auto schema with optional get parameters category, organization, page, limit


@swagger_auto_schema(
    method="get",
    operation_summary="Get items by category, organization, page and limit",
    operation_description="Retrieve the list of items matching the specified filters",
    manual_parameters=[
        openapi.Parameter(
            name="category",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False,
            description="Filter items by category"),
        openapi.Parameter(
            name="organization",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False,
            description="Filter items by organization"),
        openapi.Parameter(
            name="page",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description="Page number of the results (default: 1)"),
        openapi.Parameter(
            name="limit",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description="Number of items per page (default: 10)")
    ],
    responses={
        200: openapi.Response(
            description="List of items matching the specified filters",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "description": openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    ),
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of items matching the filters")
                }
            )
        ),
        400: "Bad Request"
    }
)
@api_view(['GET'])
@permission_classes([AllowAny, ])
def products(request):
    product_category = request.GET.get('category', None)
    organization = request.GET.get('organization', None)

    page = int(request.GET.get('page', 0))
    limit = int(request.GET.get('limit', 10))
    offset = page * limit

    if product_category is not None:
        child_categories = []

        def get_children(children: list, categories) -> list:
            filtered_children = ProductCategory.objects.filter(
                parent__in=categories)
            if filtered_children:
                children += filtered_children
                return get_children(children=children, categories=filtered_children)
            return None

        get_children(children=child_categories, categories=[product_category])

        all_categories = list(
            map(lambda x: x.id, child_categories)) + [product_category]

        products = StockProduct.objects.filter(
            product__categories__in=all_categories)
    else:
        products = StockProduct.objects.all()

    if organization is not None:
        products = products.filter(stock_point__belongs_to=organization)

    products = products.order_by('-id')[offset:offset+limit]
    serializer = ProductSerializer(products, many=True)
    return Response(AppResponse(serializer.data).body())


# create get categories
# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get top-level product categories',
#     responses={
#         200: openapi.Response(
#             description='List of top-level product categories',
#             schema=openapi.Schema(
#                 type=openapi.TYPE_ARRAY,
#                 items=openapi.Schema(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         'id': openapi.Schema(type=openapi.TYPE_INTEGER),
#                         'title': openapi.Schema(type=openapi.TYPE_STRING),
#                         'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
#                         'description': openapi.Schema(type=openapi.TYPE_STRING),
#                     }
#                 )
#             )
#         )
#     }
# )
@api_view(['GET'])
@permission_classes([AllowAny, ])
def categories(request):
    categories = ProductCategory.objects.filter(parent=None)
    serializer = ProductCategorySerializer(categories, many=True)

    return Response(AppResponse(serializer.data).body())


@api_view(['GET'])
@permission_classes([AllowAny, ])
def news(request):
    news = News.objects.filter(is_visible=True)
    serializer = NewsSerializer(news, many=True)
    return Response(AppResponse(serializer.data).body())


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_stock_points(request):
    return asyncio.run(wms_views.get_nearby_points(request))
