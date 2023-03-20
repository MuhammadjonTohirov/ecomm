from crm.models.base_model import BaseModel
from wms.models.field_type import FieldType
from wms.models.product_core import ProductCore
from django.db import models


class ProductField(BaseModel):
    product = models.ForeignKey(verbose_name='Product', to=ProductCore,
                                on_delete=models.CASCADE, null=True, blank=False, related_name='product_core')
    title = models.CharField(
        verbose_name='key', max_length=128, blank=False, default=None, null=True)
    value = models.CharField(verbose_name='Value', max_length=2048, default='')
    visible = models.BooleanField(
        verbose_name='Visible', default=True, blank=False, null=False)
    field_type = models.ForeignKey(to=FieldType, on_delete=models.SET_NULL,
                                   blank=False, default=None, null=True, name='product_field_type')

    def __str__(self):
        return f'{self.product.title} - {self.title}'
