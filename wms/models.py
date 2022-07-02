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
    image = models.ImageField(verbose_name='Image', upload_to='images/icons/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
    description = models.CharField(verbose_name='Description', max_length=512, default=None, blank=True, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'

class ProductUnit(models.Model):
    title = models.CharField(verbose_name='Title', max_length=24, default=None, blank=False, null=True)
    description = models.CharField(verbose_name='Description', max_length=512, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class ProductCore(models.Model):
    title = models.CharField(verbose_name='Title', max_length=256)

    description = models.CharField(verbose_name='Description', default=None, blank=True, max_length=1024, null=True)

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
        

class ProductField(models.Model):
    product = models.ForeignKey(verbose_name='Product', to=ProductCore, on_delete=models.CASCADE, null=True, blank=False, related_name='product_core')
    title = models.CharField(verbose_name='key', max_length=128, blank=False, default=None, null=True)
    value = models.CharField(verbose_name='Value', max_length=2048, default='')
    visible = models.BooleanField(verbose_name='Visible', default=True, blank=False, null=False)
    field_type = models.SmallIntegerField(verbose_name='Field type', name='product_field_type',
                                          choices=FieldType.__list__, default=1, null=False, blank=False)

    def __str__(self):
        return f'{self.product.title} - {self.title}'


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

    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'

    def __str__(self) -> str:
        return f'Image - {self.image.name}'

class StockProductExtraFields(models.Model):
    product = models.ForeignKey(verbose_name='StockProduct', to='StockProduct', on_delete=models.CASCADE, null=True, blank=False, related_name='stock_product_extra_fields')
    title = models.CharField(verbose_name='Title', max_length=128, default=None, blank=False, null=True)
    value = models.CharField(verbose_name='Value', max_length=2048, default='', blank=True, null=False)

    class Meta:
        verbose_name = 'Product extra field'
        verbose_name_plural = 'Product extra fields'

class StockProduct(models.Model):
    product = models.ForeignKey(ProductCore, default=False, verbose_name='Product', null=False,
                                on_delete=models.CASCADE)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=False, default=None)
    reason = models.CharField(verbose_name='Income reason', max_length=1024, blank=True, null=True)

    from_organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank=True,
                                          default=None, verbose_name='Origin')

    count = models.PositiveIntegerField(verbose_name='Quantity')
    income_price = models.FloatField(verbose_name='Income price', blank=True, default=None, null=True)
    whole_price = models.FloatField(verbose_name='Whole price', blank=True, default=None, null=True)
    single_price = models.FloatField(verbose_name='Single price')
    currency = models.SmallIntegerField(choices=enum.Currency.__list__, default=1)

    payment_method = models.SmallIntegerField(choices=enum.PaymentMethod.__list__, default=1)

    markup = models.SmallIntegerField(verbose_name='Markup', blank=True, default=0)

    session = models.CharField(verbose_name='Session', max_length=128)
    income_date = models.DateField(verbose_name='Income date')
    vat = models.PositiveIntegerField(verbose_name='VAT', choices=Vat.__list__, default=1, null=False, blank=True)
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)

    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='income_product_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='income_product_updated_by')

    class Meta:
        verbose_name = 'Product income transaction'
        verbose_name_plural = 'Product income transactions'
        
    def __str__(self):
        return f'{self.product} {self.session}'
