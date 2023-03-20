from django.test import TestCase
from wms.models.stock_point import StockPoint3
from wms.models import *
# Create your tests here.
class MainTest:
    def test_filter_stock_points(self):
        print(stock_point.objects.all())


MainTest().test_filter_stock_points()