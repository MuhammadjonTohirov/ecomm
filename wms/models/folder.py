from crm.models.User import User


from django.db import models


class Folder(models.Model):
    title = models.CharField(verbose_name='Title', max_length=128, blank=False, default=None, null=True)
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=False, default=None, null=True,
                                   related_name='folder_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='folder_updated_by')

    def __str__(self) -> str:
        return self.title