from tabnanny import verbose
from django.db import models
from django.utils import timezone

from crm.models import Address, Organization, User
from helpers import enum
from helpers.enum import Currency, FieldType, Vat

class ProductProperty(models.Model):
    body = models.JSONField(verbose_name='Product fields json')


class Warehouse(models.Model):
    title = models.CharField(verbose_name='Warehouse', max_length=512, blank=False, null=True, default=None)
    description = models.CharField(verbose_name='Description', max_length=1024, blank=True, null=True, default=None)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    belongs_to = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, default=None, blank=False)
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='wms_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='wms_updated_by')

    def __str__(self):
        return f'{self.title}'


class ProductCategory(models.Model):
    title = models.CharField(verbose_name='Title', max_length=128, default=None, blank=False, null=True)
    description = models.CharField(verbose_name='Description', max_length=512, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class ProductUnit(models.Model):
    title = models.CharField(verbose_name='Title', max_length=24, default=None, blank=False, null=True)
    description = models.CharField(verbose_name='Description', max_length=512, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class ProductCore(models.Model):
    title = models.CharField(verbose_name='Title', max_length=256)

    description = models.CharField(verbose_name='Description', default=None, blank=True, max_length=1024, null=True)

    bar_qr_code = models.CharField(verbose_name='Product code', default=None, blank=False, max_length=256, null=True,
                                   unique=True)

    unit = models.ForeignKey(to=ProductUnit, blank=False, default=None, null=True, verbose_name='Product unit',
                             on_delete=models.SET_NULL)

    categories = models.ManyToManyField(to=ProductCategory, verbose_name='Category')

    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)

    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='product_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='product_updated_by')

    def __str__(self):
        return f'{self.title} {self.bar_qr_code}'

    class Meta:
        verbose_name = 'Product Core'
        verbose_name_plural = 'Product Core'


class ProductDetails(models.Model):
    product = models.OneToOneField(to=ProductCore, verbose_name='Product', on_delete=models.CASCADE,
                                   related_name='product_core_income', default=None, blank=False, null=True,
                                   unique=True)

    description = models.CharField(max_length=2048, verbose_name='Description', default='')

    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)

    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='product_core_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='product_core_updated_by')

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'Product detail'


class ProductField(models.Model):
    product = models.ForeignKey(verbose_name='Product', to=ProductCore, on_delete=models.CASCADE, null=True, blank=False)
    title = models.CharField(verbose_name='Title', max_length=128)
    value = models.CharField(verbose_name='Value', max_length=2048, default='')
    field_type = models.SmallIntegerField(verbose_name='Field type', name='product_field_type',
                                          choices=FieldType.__list__, default=1, null=False, blank=False)


class ProductImage(models.Model):
    product = models.ForeignKey(to=ProductCore, verbose_name='Product', on_delete=models.DO_NOTHING,
                                default=None, blank=False, null=True, related_name='product_image_product')
    image = models.ImageField(verbose_name='Image', upload_to='product_images/', default=None, blank=True, null=True)
    hint = models.CharField(verbose_name='Hint', max_length=256, default=None, blank=True, null=True)
    description = models.CharField(verbose_name='Description', default=None, blank=True, max_length=1024, null=True)

    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='product_image_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='product_image_updated_by')

class StockProduct(models.Model):
    product = models.ForeignKey(ProductCore, default=False, verbose_name='Product', null=False,
                                on_delete=models.CASCADE)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=False, default=None)
    reason = models.CharField(verbose_name='Income reason', max_length=1024, blank=True, null=True)

    from_organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank=True,
                                          default=None, verbose_name='Origin')

    count = models.PositiveIntegerField(verbose_name='Quantity')
    income_price = models.FloatField(verbose_name='Income price')
    whole_price = models.FloatField(verbose_name='Whole price')
    single_price = models.FloatField(verbose_name='Single price')
    currency = models.SmallIntegerField(choices=enum.Currency.__list__, default=1)

    payment_method = models.SmallIntegerField(choices=enum.PaymentMethod.__list__, default=1)

    markup = models.SmallIntegerField(verbose_name='Markup', blank=True, default=0)

    session = models.CharField(verbose_name='Session', max_length=128)
    income_date = models.DateField(verbose_name='Income date')
    vat = models.PositiveIntegerField(verbose_name='VAT', choices=Vat.__list__, default=1, null=False, blank=False)
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)

    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='income_product_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='income_product_updated_by')

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
        
    def __str__(self):
        return f'{self.product} {self.session}'
