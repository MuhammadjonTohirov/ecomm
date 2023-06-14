from django.db import models
from wms.models.product_core import ProductCore
from crm.models.base_model import BaseModel


class ProductCoreImage(BaseModel):
    product = models.ForeignKey(verbose_name='Product', to=ProductCore,
                                on_delete=models.CASCADE, null=True, blank=False, related_name='product_core_image')
    image = models.ImageField(verbose_name='Image', upload_to='product_core_images', null=True, blank=False)
    # create sequence field for sorting images, and it should be unique and required and auto increment
    sequence = models.IntegerField(verbose_name='Sequence', null=True, blank=False, unique=True)
