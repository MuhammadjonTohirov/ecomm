from itertools import count
from time import sleep
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import render

from crm.models.organization import Organization
from helpers.responses import AppResponse
from wms.models.product_core import ProductCore
from wms.models.stock_product import MergedProductsInStock, StockInProduct
from .models.news import News
from .models.trade import Trade, TradeItem, TradeSession
from .serializers import TradeSessionSerializer
from sales.serializers import NewsSerializer, ProductCategorySerializer, ProductSerializer
from wms.models.product_category import ProductCategory

# rest framework
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

        products = StockInProduct.objects.filter(
            product__categories__in=all_categories)
    else:
        products = StockInProduct.objects.all()

    if organization is not None:
        products = products.filter(stock_point__belongs_to=organization)

    products = products.order_by('-id')[offset:offset+limit]
    serializer = ProductSerializer(products, many=True)
    return Response(AppResponse(serializer.data).body())


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def products_at_stockpoint(request):
    import json
    stock_point_id = request.data.get('stock_point_id', None)
    search = request.data.get('search', None)
    
    if stock_point_id is None:
        return Response(AppResponse('stock_point_id is required').error_body())

    product_list = MergedProductsInStock.objects.filter(stock_point__id=stock_point_id)\
    
    if search is not None:
        product_list = product_list.filter(product__title__icontains=search) \
            | product_list.filter(product__bar_qr_code__icontains=search)
        
    if product_list is None or product_list.count() == 0:
        return Response(AppResponse('No products found').error_body())
    
    def get_stock_products_by(product: MergedProductsInStock, stock_point_id: int):
        transactions_str = product.transactions
        transactions_json = json.loads(transactions_str)
        transactions = list(map(lambda x: x, transactions_json))
        _products = StockInProduct.objects.filter(id__in=transactions).filter(actual_quantity__gt=0)
        return _products
    
    products_in_stock = list(map(lambda x: get_stock_products_by(x, stock_point_id), product_list))
    
    # flat map products_in_stock
    actual_products_in_stock = [product for products in products_in_stock for product in products]

    serializer = ProductSerializer(actual_products_in_stock, many=True)
    return Response(AppResponse(serializer.data).body())


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
    import wms.views as wms_views
    return asyncio.run(wms_views.get_nearby_points(request))


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def open_new_session(request):
    import wms.models as wms_models
    import crm.models as crm_models
    from sales.actions import TradeSessionAction

    stock_point_id = request.data.get('stock_point_id', None)
    user = request.user
    try:
        stock_point = wms_models.stock_point.StockPoint3.objects.filter(
            id=stock_point_id).first()

        _employee = crm_models.employee.OrganizationEmployee.objects.filter(
            user=user.username).first()

        _session = TradeSessionAction(
            stock_point=stock_point, opened_by=_employee, closed_by=None, open_date=timezone.now(), close_date=None).create()

        serializer = TradeSessionSerializer(_session, many=False)
        return Response(AppResponse(serializer.data).body())
    except Exception as e:
        # convert e into string
        message = str(e)
        return Response(AppResponse(message).error_body())


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def close_session(request):
    try:
        import crm.models as crm_models

        session_id = request.data.get('session_id', None)
        user = request.user

        _employee = crm_models.employee.OrganizationEmployee.objects.filter(
            user=user.username).first()

        session = TradeSession.objects.get(id=session_id)

        if session.closed_by is None:
            session.closed_by = _employee
            session.close_date = timezone.now()
            session.updated_by = user
            session.updated_date = timezone.now()
            session.save()
        _serializer = TradeSessionSerializer(session, many=False)
        return Response(AppResponse(_serializer.data).body())
    except Exception as e:
        # convert e into string
        message = str(e)
        return Response(AppResponse(message).error_body())


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_active_session(request):
    import crm.models as crm_models
    import wms.models as wms_models

    user = request.user
    _employee = crm_models.employee.OrganizationEmployee.objects.filter(
        user=user.username).first()

    stock_points = wms_models.stock_point.StockPoint3.objects.filter(
        belongs_to=_employee.organization)

    sessions = TradeSession.objects.filter(
        closed_by=None).filter(stock_point__in=stock_points)

    if sessions.exists():
        _serializer = TradeSessionSerializer(sessions.first(), many=False)
        return Response(AppResponse(_serializer.data).body())

    return Response(AppResponse('No active session found').error_body())

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def do_sale(request):
    from crm.models.employee import OrganizationEmployee
    from crm.models.client import Client
    session_id = request.data.get('session_id', None)
    products = request.data.get('products', None)
    total_amount = request.data.get('total_amount', None)
    cashier_id = request.data.get('cashier_id', None)
    client_id = request.data.get('client_id', None)
    payment_method = request.data.get('payment_method', None) 
    payment_amount = request.data.get('payment_amount', None)
    # trade_date = now
    trade_date = timezone.now()
    
    session = TradeSession.objects.get(id=session_id)
    cashier = OrganizationEmployee.objects.get(id=cashier_id)
    
    client = None
    if client_id is not None and client_id != 0:
        client = Client.objects.get(id=client_id)
        
    trade = Trade.objects.create(
        session = session,
        total_amount = total_amount,
        cashier = cashier,
        client = client,
        payment_method = payment_method,
        payment_amount = payment_amount,
        trade_date = trade_date
    )
    
    def set_actual_quantity(item: StockInProduct, quantity: int):
        import json
        
        diff = item.actual_quantity - quantity
        
        item.actual_quantity = quantity
        
        mpins = MergedProductsInStock.objects.filter(product=item.product, stock_point=item.stock_point).first()
        mpins.actual_quantity = mpins.actual_quantity - diff
        
        if item.actual_quantity == 0:
            # delete single item from transactions which is id list of stockinproduct
            mpins.transactions = json.dumps([x for x in json.loads(mpins.transactions) if x != item.id])
        mpins.save()
        item.save()
    
    for prod in products:
        stock_product_id = prod['stock_product_id']
        product = StockInProduct.objects.get(id=stock_product_id)
        quantity = prod['quantity']
        price = prod['price']
        
        TradeItem.objects.create(
            trade = trade,
            product = product,
            quantity = quantity,
            price = price
        )
        
        set_actual_quantity(product, product.actual_quantity - quantity)
    
    return Response(AppResponse('Sale is done').body())