from django.urls import path, include
from rest_framework import routers

from crm import views
import sales.views as sales_views
urlpatterns = [
    path('dashboard', sales_views.dashboard),
    path('other', sales_views.other),
    path('products', sales_views.products),
    path('categories', sales_views.categories),
    path('news', sales_views.news),
    path('get_stock_points', sales_views.get_stock_points),
    path('nearby_shops', sales_views.get_stock_points),
    path('open_new_session', sales_views.open_new_session),
    # close_session
    path('close_session', sales_views.close_session),
    # get_active_session
    path('get_active_session', sales_views.get_active_session),
    # products_at_stockpoint
    path('products_at_stockpoint', sales_views.products_at_stockpoint),
    path('do_sale', sales_views.do_sale),
]