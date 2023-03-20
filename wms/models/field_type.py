from crm.models.User import User


from django.db import models


class FieldType(models.Model):
    title = models.CharField(max_length=255, verbose_name='Field type title')
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='field_type_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='field_type_updated_by')

    def __str__(self) -> str:
        return self.title