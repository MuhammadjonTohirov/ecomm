from crm.models.organization import Organization
from crm.models.User import User
from helpers import enum
from helpers.enum import Vat
from wms.models.stock_point import StockPoint3
from wms.models.Image import Image
from wms.models.product_core import ProductCore
from django.db import models


class StockProduct(models.Model):
    product = models.ForeignKey(
        ProductCore, default=False, verbose_name='Product', null=False, on_delete=models.CASCADE)
    stock_point = models.ForeignKey(
        StockPoint3, on_delete=models.SET_NULL, null=True, blank=True, default=None, name="stock_point")
    reason = models.CharField(
        verbose_name='Income reason', max_length=1024, blank=True, null=True)
    from_organization = models.ForeignKey(
        Organization, on_delete=models.DO_NOTHING, null=True, blank=True, default=None, verbose_name='Origin')
    count = models.PositiveIntegerField(
        verbose_name='Quantity', null=True, blank=True, default=None)
    income_price = models.FloatField(
        verbose_name='Income price', blank=True, default=None, null=True)
    whole_price = models.FloatField(
        verbose_name='Whole price', blank=True, default=None, null=True)
    single_price = models.FloatField(verbose_name='Single price')
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL,
                                 null=True, blank=True, default=None, verbose_name='Discount')
    currency = models.SmallIntegerField(
        choices=enum.Currency.__list__, default=1)

    payment_method = models.SmallIntegerField(
        choices=enum.PaymentMethod.__list__, default=1)

    markup = models.SmallIntegerField(
        verbose_name='Markup', blank=True, default=0)

    session = models.CharField(
        verbose_name='Session', max_length=128, null=True, blank=True, default=None)
    income_date = models.DateField(
        verbose_name='Income date',  null=True, blank=True, default=None)
    vat = models.PositiveIntegerField(
        verbose_name='VAT', choices=Vat.__list__, default=1, null=False, blank=True)
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)

    updated_date = models.DateTimeField(
        verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='income_product_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='income_product_updated_by')

    class Meta:
        verbose_name = 'Product income transaction'
        verbose_name_plural = 'Product income transactions'
        unique_together = ('product', 'session')

    def __str__(self):
        return f'{self.product} {self.session}'

    def save(self):
        super(StockProduct, self).save()
