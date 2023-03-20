from django.db import models
from crm.models.base_model import BaseModel
from wms.models.stock_product import StockProduct
# import timezone
from django.utils import timezone

class Discount(BaseModel):
    title = models.CharField(
        verbose_name='Title', max_length=128, blank=False, default=None, null=True)

    by_percentage = models.SmallIntegerField(
        verbose_name='Percentage', blank=True, default=None, null=True)

    valid_until = models.DateTimeField(
        verbose_name='Valid until', blank=True, default=None, null=True)

    def __str__(self) -> str:
        return self.title

    def is_valid(self) -> bool:
        return self.valid_until > timezone.now() if self.valid_until else True

