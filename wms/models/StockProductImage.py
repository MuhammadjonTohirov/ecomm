from django.db import models


class StockProductImage(models.Model):
    product = models.ForeignKey(verbose_name='StockProduct', to='StockProduct', on_delete=models.CASCADE,
                                null=True, blank=False, related_name='stock_product_image')
    image = models.ImageField(
        verbose_name='Image', upload_to='images', default=None, blank=False, null=True)

    caption = models.CharField(verbose_name='Caption', max_length=512, default=None, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'
