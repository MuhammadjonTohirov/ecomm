from ast import For
from django.utils import timezone
from rest_framework import serializers
from django.core import serializers as django_serializers
from django.forms.models import model_to_dict
from helpers.enum import FieldType

from wms.models import ProductCategory, ProductField, ProductImage, StockProduct
from wms.serializers import ProductCoresSerializer

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
        model = StockProduct
        fields = ('id', 'product', 'count', 'income_price', 'whole_price', 'single_price', 'session',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        images = ProductImage.objects.filter(product=instance.product)
        fields = ProductField.objects.filter(product=instance.product)
        data['images'] = images.values('image', 'hint', 'description')
        
        def update_fild_type(field):
            return {
                'title': field['title'],
                'type': FieldType.typeInfo(field['product_field_type']),
                'value': field['value'],
            }

        data['fields'] = fields.values('title', 'value', 'product_field_type')

        data['fields'] = map(update_fild_type, data['fields'])
        return  data
        