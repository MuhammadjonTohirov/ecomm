from django.urls import path, include
from rest_framework import routers

from wms import views

router = routers.DefaultRouter()

urlpatterns = [
    path('stock_points', views.get_stockpoints),
    path('inventory', views.get_inventory),
    path('product_transactions', views.stock_product_transactions)
]
