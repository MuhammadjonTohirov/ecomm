from crm.models.User import User
from wms.models.product_category import ProductCategory
from wms.models.product_unit import ProductUnit


from django.db import models


class ProductCore(models.Model):
    title = models.CharField(verbose_name='Title', max_length=256)

    description = models.CharField(verbose_name='Description', default=None, blank=True, max_length=1024, null=True)

    image = models.ManyToManyField(to='Image', verbose_name='Images', default=None, blank=True,)

    tag = models.CharField(verbose_name='Tag', default=None, blank=True, max_length=256, null=True)

    color = models.ForeignKey(to='Color', on_delete=models.SET_NULL, blank=True, default=None, null=True)

    bar_qr_code = models.CharField(verbose_name='Product code', default=None, blank=True, max_length=256, null=True,
                                   unique=True)

    unit = models.ForeignKey(to=ProductUnit, blank=False, default=None, null=True, verbose_name='Product unit',
                             on_delete=models.SET_NULL)

    categories = models.ManyToManyField(to=ProductCategory, verbose_name='Category', blank=True, default=None, related_name='categories')

    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)

    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='product_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='product_updated_by')

    def __str__(self):
        # short if else
        br_code = f'- {self.bar_qr_code}' if self.bar_qr_code is not None else ''
        return f'{self.title} - {self.unit} {br_code}'

    class Meta:
        verbose_name = 'Product Core'
        verbose_name_plural = 'Product List'