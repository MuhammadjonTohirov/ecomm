from crm.models.base_model import BaseModel
import crm.models.organization
from crm.models import User as crm_models
from wms.models import stock_product as wms_models


from django.db import models


class News(BaseModel):
    title = models.CharField(verbose_name='Title', max_length=512)
    description = models.CharField(verbose_name='Description', max_length=1024)
    is_visible = models.BooleanField(verbose_name='Is visible', default=True)
    image = models.CharField(
        verbose_name='Image url', max_length=512, null=True, blank=False, default=None)
    related_products = models.ManyToManyField(
        wms_models.StockProduct, blank=True)
    related_companies = models.ManyToManyField(
        crm.models.organization.Organization, blank=True)

    is_active_until = models.DateTimeField(
        verbose_name='Is active until', blank=False, null=True, default=None)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News list'
