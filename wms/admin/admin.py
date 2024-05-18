# from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from crm.admin.base_admin_model import BaseAdminModel
from wms.models.folder import Folder
from wms.models.product_core_images import ProductCoreImage
from wms.models.product_field import ProductField
from wms.models.field_type import FieldType
from wms.models.Discount import Discount
from wms.models.product_category import ProductCategory
from wms.models.product_core import ProductCore
from wms.models.product_unit import ProductUnit
# import ProductUnitConverter
from wms.models.product_unit_converter import ProductUnitConverter
from django.utils.html import format_html
import socket


class ProductFieldInline(admin.TabularInline):
    model = ProductField
    can_delete = True
    verbose_name_plural = 'Field list'
    extra: int = 1
    max_num: int = 20
    fields = ('title', 'value', 'visible', 'product_field_type')
    fk_name = 'product'


class ProductCoreImageInline(admin.TabularInline):
    model = ProductCoreImage
    can_delete = True
    verbose_name_plural = 'Image list'
    extra: int = 1
    max_num: int = 20
    fields = ('image', 'sequence')
    fk_name = 'product'


@admin.register(FieldType)
class FieldTypeAdmin(admin.ModelAdmin):
    model = FieldType
    list_display = ('id', 'title')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    model = Folder
    list_display = ('title', )


@admin.register(ProductCore)
class ProductCoreAdmin(admin.ModelAdmin):
    inlines = (ProductFieldInline, ProductCoreImageInline, )
    search_fields = ('title', 'id', 'bar_qr_code')
    list_display = ('title', 'image', 'id', 'bar_qr_code')
    list_filter = ('title', 'bar_qr_code')
    filter_horizontal = ('categories', )


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'description', 'image')


@admin.register(Discount)
class DiscountAdmin(BaseAdminModel):
    list_display = ['title', 'by_percentage',
                    'valid_until', 'created_by', 'updated_by']
    list_filter = ['valid_until', 'created_by']
    search_fields = ['title', 'created_by__username']

    fieldsets = fieldsets = [
        (('Discount'), {'fields': ('title', 'by_percentage', 'valid_until')}),
    ] + BaseAdminModel.fieldsets

    def is_valid(self, obj):
        return obj.is_valid()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user.id)


@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'description')

    # valid for only admin
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user.id)
