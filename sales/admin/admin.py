from django.contrib import admin
from django.http import HttpRequest
from crm.admin.base_admin_model import BaseAdminModel
from sales.models.cart import Cart
from sales.models.news import News
from sales.models.order import Order
from sales.models.order_state import OrderState
from sales.models.trade import TradeSession


@admin.register(OrderState)
class OrderStateAdmin(BaseAdminModel):
    model = OrderState
    list_display = ('title',)

    fieldsets = [('OrderState', {'fields': ['title']})
                 ] + BaseAdminModel.fieldsets


class OrderAdminInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('product', 'count', 'user',)
    can_delete = True


@admin.register(Cart)
class CartAdmin(BaseAdminModel):
    inlines = [OrderAdminInline]
    model = Cart
    list_display = ('id', 'user', 'created_date', 'updated_date', 'is_active',)
    fieldsets = [('Cart', {'fields': ['user', 'is_active']})
                 ] + BaseAdminModel.fieldsets

    # delete all orders in cart
    def delete_queryset(self, request: HttpRequest, queryset) -> None:
        for cart in queryset:
            # delete all orders in cart
            Order.objects.filter(cart=cart).delete()
            cart.delete()


@admin.register(Order)
class OrderAdmin(BaseAdminModel):
    model = Order
    list_display = ('product', 'cart', 'count', 'user',)

    fieldsets = [('Order', {'fields': ['product', 'cart',
                  'count', 'user']})] + BaseAdminModel.fieldsets

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def delete_queryset(self, request: HttpRequest, queryset) -> None:
        for cart in queryset:
            cart.delete()


@admin.register(News)
class NewsAdmin(BaseAdminModel):
    model = News
    list_display = ('title',  'description', 'is_visible',
                    'image', 'created_date', 'updated_date',)
    list_filter = ('is_visible',)
    search_fields = ('title', 'description',)
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'updated_date',)
    filter_horizontal = ('related_products', 'related_companies',)

    fieldsets = [('News', {'fields': ['title', 'description', 'is_visible', 'image',
                 'related_products', 'related_companies']})] + BaseAdminModel.fieldsets
