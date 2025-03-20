from wms.models.Discount import Discount
from wms.models.stock_point import StockPoint3
from wms.models.stock_product import MergedProductsInStock, StockInProduct
from django.contrib import admin

from wms.models.StockProductExtraFields import StockProductExtraFields
from wms.models.StockProductImage import StockProductImage
# import ProductUnitConverter
from wms.models.product_unit_converter import ProductUnitConverter

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


class ProductUnitConverterInline(admin.TabularInline):
    model = ProductUnitConverter
    can_delete = True
    verbose_name_plural = 'Unit converter list'
    extra: int = 1
    max_num: int = 20
    fields = ('title', 'conversion_rate')
    pk_name = 'product'


@admin.register(StockInProduct)
class IncomingProductAdmin(admin.ModelAdmin):
    inlines = (StockProductExtraFieldsInline, ProductUnitConverterInline,)
    list_display = ('product', 'id', 'stock_point',
                    'count', 'actual_quantity', 'whole_price', 'single_price', 'income_price', 'custom_barcode', 'session',)

    search_fields = ('product__title', 'product__id', 'stock_point__title',
                     'stock_point__id', 'session__title', 'session__id',)

    # filter by stock point
    list_filter = (
        ('stock_point', admin.RelatedOnlyFieldListFilter), 'product', 'session',)
    
    actions = []
    actions_on_top = False
    actions_on_bottom = False

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

    def get_filter_list(self, request):
        if request.user.is_superuser:
            return self.list_filter

        return (
            ('stock_point', admin.RelatedOnlyFieldListFilter),
            'product',
            'session',
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(stock_point__belongs_to__owner__user=request.user.id)

    def save_model(self, request, obj: StockInProduct, form, change):
        import json

        if obj.actual_quantity is None:
            obj.actual_quantity = obj.count
            
        old_quantity = 0
        old_actual_quantity = 0
        if change:
            old = StockInProduct.objects.get(id = obj.id);
            old_quantity = old.count or 0
            old_actual_quantity = old.actual_quantity or 0
        
        if obj.actual_quantity > obj.count:
            obj.actual_quantity = obj.count
            
        super().save_model(request, obj, form, change)
        merged_product, created = MergedProductsInStock.objects.get_or_create(
            product=obj.product,
            stock_point=obj.stock_point
            )
        
        if created:
            merged_product.total_quantity = obj.count
            merged_product.actual_quantity = obj.actual_quantity
        else:
            quantity_diff = (obj.count or 0) - old_quantity
            actual_quantity_diff = (obj.actual_quantity or 0) - old_actual_quantity
            merged_product.total_quantity = quantity_diff + (merged_product.total_quantity or 0)
            merged_product.actual_quantity = actual_quantity_diff + (merged_product.actual_quantity or 0)
        
        if merged_product.actual_quantity > merged_product.total_quantity:
                merged_product.actual_quantity = merged_product.total_quantity
                
        transactions = json.loads(merged_product.transactions) if merged_product.transactions else []
        if obj.id not in transactions:
            transactions.append(obj.id)
        merged_product.transactions = json.dumps(transactions)
        merged_product.save()
        
    # override delete method
    def delete_model(self, request, obj: StockInProduct):
        import json
        merged_product = MergedProductsInStock.objects.get(
            product=obj.product,
            stock_point=obj.stock_point
            )
        if merged_product is not None:
            merged_product.total_quantity = (merged_product.total_quantity or 0) - (obj.count or 0)
            merged_product.actual_quantity = (merged_product.actual_quantity or 0) - (obj.actual_quantity or 0)
                
            transactions = json.loads(merged_product.transactions) if merged_product.transactions else []
            if obj.id in transactions:
                transactions.remove(obj.id)
            merged_product.transactions = json.dumps(transactions)
            merged_product.save()
        super().delete_model(request, obj)
        


@admin.register(MergedProductsInStock)
class MergedProductsInStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock_point', 'total_quantity', 'actual_quantity', 'transactions')
    # config search
    search_fields = ('product__title', 'product__id')
    
    # disable create new item
    def has_add_permission(self, request):
        return False
    
    # hide delete button
    def has_delete_permission(self, request, obj=None):
        return False
    
    # hide save button
    def has_change_permission(self, request, obj=None):
        return False
    
    # disable save
    def save_model(self, request, obj, form, change):
        pass
