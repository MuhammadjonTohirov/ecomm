from django.urls import path, include
from rest_framework import routers

from wms import views

router = routers.DefaultRouter()

urlpatterns = [
    path('stock_points', views.get_stockpoints),
]
