from django.urls import path, include
from rest_framework import routers

from crm import views
import sales.views as sales_views
urlpatterns = [
    path('', sales_views.index_2),
    path('other', sales_views.other),
    path('products', sales_views.products),
    path('categories', sales_views.categories),
    path('news', sales_views.news),
    path('get_stock_points', sales_views.get_stock_points),
    path('nearby_shops', sales_views.get_stock_points),
]