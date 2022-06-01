from django.urls import path, include
from rest_framework import routers

from crm import views
import sales.views as sales_views
urlpatterns = [
    path('', sales_views.index),
    path('other', sales_views.other),
    path('products', sales_views.products),
    path('categories', sales_views.categories),
]