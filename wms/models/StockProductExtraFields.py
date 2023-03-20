from django.db import models


class StockProductExtraFields(models.Model):
    product = models.ForeignKey(verbose_name='StockProduct', to='StockProduct', on_delete=models.CASCADE,
                                null=True, blank=False, related_name='stock_product_extra_fields')
    title = models.CharField(
        verbose_name='Title', max_length=128, default=None, blank=False, null=True)
    value = models.CharField(
        verbose_name='Value', max_length=2048, default='', blank=True, null=False)

    class Meta:
        verbose_name = 'Product extra field'
        verbose_name_plural = 'Product extra fields'
