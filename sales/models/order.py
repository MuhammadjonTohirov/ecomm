from crm.models import User as crm_models
from crm.models.base_model import BaseModel
from sales.models.cart import Cart
from sales.models.order_state import OrderState
from wms.models import stock_product as wms_models
from django.db import models


class Order(BaseModel):
    # need to update product foreign key - merge products count into one field
    cart = models.ForeignKey(
        Cart, on_delete=models.DO_NOTHING, null=True, default=None, blank=False)
    product = models.ForeignKey(
        wms_models.StockProduct, on_delete=models.DO_NOTHING, null=True)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(
        crm_models.User, on_delete=models.DO_NOTHING, null=True)
    state = models.ForeignKey(
        OrderState, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'{self.cart.user.username} {self.product.product} {self.count}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
