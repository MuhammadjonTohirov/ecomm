from crm.models.organization import Organization
from crm.models.User import User
from crm.models.models import OrganizationAddress, Person
from django.db import models


class StockPoint3(models.Model):
    title = models.CharField(verbose_name='Stock Point',
                             max_length=512, blank=False, null=True, default=None)
    description = models.CharField(
        verbose_name='Description', max_length=1024, blank=True, null=True, default=None)
    address = models.ForeignKey(
        OrganizationAddress, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    assigned_director = models.ForeignKey(to=Person, on_delete=models.SET_NULL, blank=True,
                                          default=None, null=True, related_name='stock_point_assigned_director')
    belongs_to = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, default=None, blank=False)
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(
        verbose_name='Updated date', blank=True, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='wms_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='wms_updated_by')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Stock Point.'
        verbose_name_plural = 'Stock Points'
