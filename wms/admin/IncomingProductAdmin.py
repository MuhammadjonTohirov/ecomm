from wms.models.Discount import Discount
from wms.models.stock_point import StockPoint3
from wms.models.stock_product import StockProduct
from django.contrib import admin

from wms.models.StockProductExtraFields import StockProductExtraFields
from wms.models.StockProductImage import StockProductImage


class StockProductExtraFieldsInline(admin.TabularInline):
    model = StockProductExtraFields
    can_delete = True
    extra: int = 1
    max_num: int = 20
    verbose_name_plural = 'Extra field list'
    show_change_link = True
    fk_name = 'product'


class StockProductImageInline(admin.TabularInline):
    model = StockProductImage
    can_delete = True
    extra = 1
    max_num = 4
    verbose_name_plural = 'Image list'
    show_change_link = True
    fk_name = 'product'


@admin.register(StockProduct)
class IncomingProductAdmin(admin.ModelAdmin):
    inlines = (StockProductExtraFieldsInline, StockProductImageInline,)
    list_display = ('product', 'id', 'stock_point', 'is_countable',
                    'count', 'income_price', 'whole_price', 'single_price', 'session',)

    def is_countable(self, obj):
        return obj.count is not None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'stock_point' and not request.user.is_superuser:
            kwargs['queryset'] = StockPoint3.objects.filter(
                belongs_to__owner__user=request.user.id)

        if db_field.name == 'discount' and not request.user.is_superuser:
            kwargs['queryset'] = Discount.objects.filter(
                created_by=request.user.id)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(stock_point__belongs_to__owner__user=request.user.id)
