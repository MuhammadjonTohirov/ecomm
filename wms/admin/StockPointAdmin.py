from wms.models.stock_point import StockPoint3


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

    # get queryset related to user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(belongs_to__belongs_to__user=request.user.id)

    # has add permission
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        return StockPoint3.objects.filter(belongs_to__belongs_to__user=request.user.id).count() < 1
