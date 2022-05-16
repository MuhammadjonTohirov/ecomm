from rest_framework import serializers

from wms.models import ProductCore, ProductImage, ProductUnit

class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = ('title', )

class ProductCoresSerializer(serializers.ModelSerializer):
    unit = UnitsSerializer(many=False)

    class Meta:
        model = ProductCore
        fields = ('id', 'title', 'bar_qr_code', 'unit', 'description',)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image',)
