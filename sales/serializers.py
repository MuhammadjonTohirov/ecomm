from ast import For
from django.utils import timezone
from rest_framework import serializers
from django.core import serializers as django_serializers
from django.forms.models import model_to_dict
from wms.models.product_category import ProductCategory

from wms.models.stock_product import StockInProduct
from .models.news import News

from wms.models.product_field import ProductField
from wms.serializers import ProductCoresSerializer
from .models.trade import TradeSession
from wms.models.product_unit_converter import ProductUnitConverter

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'description', 'image', 'parent')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        subs = ProductCategorySerializer(ProductCategory.objects.filter(parent=data['id']), many=True)
        data['subcategories'] = subs.data
        return data

class ProductSerializer(serializers.ModelSerializer):
    product = ProductCoresSerializer()
    
    class Meta:
        model = StockInProduct
        fields = ('id', 'product', 'count', 'actual_quantity', 'income_price', 'whole_price', 'single_price', 'session',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # images = ProductImage.objects.filter(product=instance.product)
        fields = ProductField.objects.filter(product=instance.product)
        # data['images'] = images.values('image', 'hint', 'description')
        unit_converters = ProductUnitConverter.objects.filter(product=instance)
        def update_fild_type(field):
            return {
                'title': field['title'],
                'type': field['product_field_type'],
                'value': field['value'],
                'visible': field['visible']
            }

        data['fields'] = fields.values('title', 'value', 'product_field_type', 'visible')
        data['fields'] = map(update_fild_type, data['fields'])
        data['unit_converters'] = unit_converters.values('title', 'conversion_rate')
        return  data
        

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'description', 'image', 'is_active_until', 'is_visible')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        if data['is_visible'] is False:
            del data['title']
            del data['description']
            del data['image']
            del data['is_active_until']
        return data
    
class TradeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeSession
        fields = ('id', 'stock_point', 'opened_by', 'closed_by', 'open_date', 'close_date')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_open'] = instance.close_date is None
        return data