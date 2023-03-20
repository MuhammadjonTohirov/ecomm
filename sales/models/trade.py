from django.db import models
from crm.models.base_model import BaseModel

from wms.models.stock_product import StockProduct


class Trade(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Trade title')
    code = models.CharField(max_length=255, verbose_name='Trade code')

    def __str__(self) -> str:
        return self.title


class ProductInTrade(BaseModel):
    product = models.ForeignKey(to=StockProduct, on_delete=models.CASCADE, blank=False,
                                default=None, null=True, related_name='product_in_trade_product')
    trade = models.ForeignKey(to=Trade, on_delete=models.CASCADE, blank=False,
                              default=None, null=True, related_name='product_in_trade_trade')
    # customer = 