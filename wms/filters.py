import django_filters

from wms.models.stock_point import StockPoint3

class StockPointFilters(django_filters.FilterSet):
    
    class Meta:
        model = StockPoint3
        fields = {
            
        }