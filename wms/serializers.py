from rest_framework import serializers
from crm.serializers import OrganizationAddressSerializer, OrganizationSerializer
from helpers.methods import Methods
from wms.models.stock_point import StockPoint3
from wms.models.stock_product import StockInProduct
from wms.models.product_core import ProductCore

from wms.models.product_unit import ProductUnit
from wms.models.product_category import ProductCategory


class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = ('id', 'title',)

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'title',)

class ProductCoresSerializer(serializers.ModelSerializer):
    unit = UnitsSerializer(many=False)
    categories = ProductCategorySerializer(many=True)
    class Meta:
        model = ProductCore
        fields = ('id', 'categories', 'color', 'image', 'title',
                  'bar_qr_code', 'unit', 'description',)
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class StockPointSerializer(serializers.ModelSerializer):
    belongs_to = OrganizationSerializer(many=False)
    address = OrganizationAddressSerializer()

    def __init__(self, instance=None, data=..., destination=''):
        super().__init__(instance, data)
        self.destination = destination

    class Meta:
        model = StockPoint3
        fields = ('id', 'title', 'assigned_director',
                  'description', 'address', 'belongs_to')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['address']['distance'] = Methods.distance(
            (data['address']['latitude'], data['address']['longitude']),
            self.destination,
        )
        return data


class StockPointDefaultSerializer(serializers.ModelSerializer):
    address = OrganizationAddressSerializer()

    class Meta:
        model = StockPoint3
        fields = ('id', 'title', 'assigned_director',
                  'description', 'address', 'belongs_to')
