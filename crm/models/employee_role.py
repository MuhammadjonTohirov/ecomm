from crm.models.base_model import BaseModel
from django.contrib.auth.models import Permission


from django.db import models


class Role(BaseModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, blank=True, null=True)
    def __str__(self):
        return self.title

    @classmethod
    def director(cls) -> 'Role':
        return Role.objects.get_or_create(title='Director')
    