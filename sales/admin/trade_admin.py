from django.contrib import admin

from django.contrib import messages
from crm.admin.base_admin_model import BaseAdminModel
from sales.models.trade import Trade, TradeItem, TradeSession


@admin.register(TradeSession)
class TradeSessionAdmin(BaseAdminModel):
    model = TradeSession

    def is_open(self, obj):
        return obj.close_date is None

    list_display = ('stock_point', 'id', 'opened_by', 'closed_by',
                    'open_date', 'close_date', 'is_open')

    list_filter = ('stock_point', 'opened_by', 'closed_by',)
    search_fields = ('stock_point__title', )
    ordering = ('-open_date',)
    readonly_fields = ('open_date', 'close_date',)

    fieldsets = [('TradeSession', {'fields': ['stock_point', 'opened_by', 'closed_by',
                 'open_date', 'close_date']})] + BaseAdminModel.fieldsets
        
    # create if stock_point, opened_by is unqiue and close_date is null
    def save_model(self, request, obj, form, change):
        if obj.stock_point is None:
            # promt "don't raise Exception, just show message"
            raise Exception('Stock point is required')

        _sessions = TradeSession.objects.filter(
            stock_point=obj.stock_point, closed_by=None, opened_by=obj.opened_by, close_date=None)

        if _sessions.count() > 0:
            messages.error(request, 'Session is already opened')
            messages.set_level(request, messages.ERROR)
            return

        obj.save()
        
# tabular in,ine for TradeItem
class TradeItemInline(admin.TabularInline):
    model = TradeItem
    extra = 1
    fields = ('product', 'quantity', 'price')
    show_change_link = True
    verbose_name_plural = 'Trade Items'
    verbose_name = 'Trade Item'
    fk_name = 'trade'

@admin.register(Trade)
class TradeAdmin(BaseAdminModel):
    model = Trade
    inlines = (TradeItemInline, )
    fieldsets = [('Trade', {'fields': ['session', 'total_amount', 'payment_amount', 'cashier', 'payment_method', 'trade_date']})] + BaseAdminModel.fieldsets
    list_display = ('session', 'total_amount', 'cashier', 'payment_method', 'trade_date',)
    # list_display = ('session', 'total_amount', 'cashier', 'payment_method', 'trade_date',) + BaseAdminModel.list_display
