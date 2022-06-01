# from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from wms.models import *

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address')

class ProductFieldInline(admin.TabularInline):
    model = ProductField
    can_delete = True
    verbose_name_plural = 'Field list'
    extra: int = 1
    max_num: int = 5
    fk_name = 'product'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    can_delete = True
    extra: int = 1
    max_num: int = 5
    verbose_name_plural = 'Image list'
    fk_name = 'product'

@admin.register(ProductCore)
class ProductCoreInline(admin.ModelAdmin):
    inlines = (ProductImageInline, ProductFieldInline)
    list_display = ('title', 'bar_qr_code',)


@admin.register(ProductDetails)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')


@admin.register(StockProduct)
class IncomingProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'count', 'income_price', 'whole_price', 'single_price', 'session',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')

