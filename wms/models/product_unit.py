from django.db import models
# import BaseModel
from crm.models.base_model import BaseModel


class ProductUnit(models.Model):
    title = models.CharField(
        verbose_name='Title', max_length=24, default=None, blank=False, null=True)
    description = models.CharField(
        verbose_name='Description', max_length=512, default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Base Product unit'
        verbose_name_plural = 'Base Product units'
        db_table = 'wms_productunit'
        ordering = ['title']
