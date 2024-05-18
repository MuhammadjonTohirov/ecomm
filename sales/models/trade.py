from django.db import models
from crm.models.base_model import BaseModel


class TradeSession(BaseModel):
    stock_point = models.ForeignKey(to='wms.StockPoint3', on_delete=models.CASCADE,
                                    blank=False, default=None, null=False, related_name='trade_session_stock_point')

    opened_by = models.ForeignKey(to='crm.OrganizationEmployee', on_delete=models.CASCADE, blank=False,
                                  default=None, null=False, related_name='trade_session_opened_by')
    
    closed_by = models.ForeignKey(to='crm.OrganizationEmployee', on_delete=models.CASCADE, blank=True,
                                  default=None, null=True, related_name='trade_session_closed_by')

    open_date = models.DateTimeField(verbose_name='Trade open date', null=True, default=None)

    close_date = models.DateTimeField(verbose_name='Trade close date', null=True, default=None)
    
    # unique with
    class Meta:
        unique_together = ('stock_point', 'opened_by', 'close_date')
        
    def __str__(self) -> str:
        return f'{self.stock_point.title} {self.open_date} {self.close_date}'


class Trade(BaseModel):
    session = models.ForeignKey(to=TradeSession, on_delete=models.CASCADE, blank=False, default=None, null=False,
                                related_name='trade_session')
    
    total_amount = models.DecimalField(verbose_name='Total amount', max_digits=10, decimal_places=2, default=0.00)
    
    cashier = models.ForeignKey(to='crm.OrganizationEmployee', on_delete=models.CASCADE, blank=False, default=None, null=False,
                                related_name='trade_cashier')
    
    client = models.ForeignKey(to='crm.Client', on_delete=models.DO_NOTHING, blank=True, default=None, null=True,)
    
    payment_method = models.SmallIntegerField(default=1) # 1 - cash, 2 - card, 3 - both of them
    
    payment_amount = models.DecimalField(verbose_name='Payment amount', max_digits=10, decimal_places=2, default=0.00)
    
    trade_date = models.DateTimeField(verbose_name='Trade date', null=True, default=None)

class TradeItem(BaseModel):
    trade = models.ForeignKey(to=Trade, on_delete=models.CASCADE, blank=False, default=None, null=False,
                              related_name='trade')
    
    product = models.ForeignKey(to='wms.StockInProduct', on_delete=models.CASCADE, blank=False, default=None, null=False,
                                related_name='trade_product')
    
    quantity = models.FloatField(verbose_name='Quantity', null=True, blank=False, default=0)
    
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2, default=0.00)
    
    # unique with
    class Meta:
        unique_together = ('trade', 'product')