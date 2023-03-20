# from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from crm.admin.base_admin_model import BaseAdminModel
from wms.models.folder import Folder
from wms.models.product_field import ProductField
from wms.models.field_type import FieldType
from wms.models.Discount import Discount
from wms.models.product_category import ProductCategory
from wms.models.Image import Image
from wms.models.product_core import ProductCore
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


@admin.register(FieldType)
class FieldTypeAdmin(admin.ModelAdmin):
    model = FieldType
    list_display = ('id', 'title')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    model = Folder
    list_display = ('title', )


@admin.register(Image)
class Images(admin.ModelAdmin):
    model = Image
    list_display = ('id', 'image', )


@admin.register(ProductCore)
class ProductCoreAdmin(admin.ModelAdmin):
    inlines = (ProductFieldInline, )
    search_fields = ('title', 'id', 'bar_qr_code')
    list_display = ('title', 'product_image', 'id', 'bar_qr_code')
    list_filter = ('title', 'bar_qr_code')
    filter_horizontal = ('image', 'categories')

    def product_image(self, obj: ProductCore):
        return format_html("""<img src='http://{host}:8000{url}' width='100' height='100'
                                style = 'object-fit: contain;'
                           />
                           """.format(host=socket.gethostbyname(socket.gethostname()), url=obj.image.first().image.url))


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
