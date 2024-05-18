from wms.models.stock_point import StockPoint3

from wms.models.product_unit_converter import ProductUnitConverter
from django.contrib import admin
from django.utils.html import format_html


@admin.register(StockPoint3)
class StockPointAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'description', 'address_on_map')

    def _address(self, obj: StockPoint3):
        return f'{obj.address.latitude}, {obj.address.longitude}, {obj.address.building_number}'

    def address_on_map(self, obj):
        url = f'http://www.google.com/maps/place/{obj.address.latitude}, {obj.address.longitude}'
        return format_html(f"<a href='{url}' target = '_blank'>{self._address(obj)}</a>", url=url)
