# from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from wms.models import *


@admin.register(ProductCore)
class ProductCoreInline(admin.ModelAdmin):
    list_display = ('title', 'bar_qr_code',)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address')


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'is_active')


class ProductFieldInline(admin.StackedInline):
    model = ProductField
    can_delete = True
    verbose_name_plural = 'Field list'
    fk_name = 'product'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductFieldInline, )
    list_display = ('id', 'product')


@admin.register(IncomingProduct)
class IncomingProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'income_price', 'whole_price', 'single_price', 'session',)


@admin.register(WmsIncome)
class ProductIncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'reason', 'created_date', 'created_by')

