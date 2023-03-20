from crm.models.User import User
from crm.models.base_model import BaseModel
from django.db import models


class Color(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Color title')
    code = models.CharField(max_length=255, verbose_name='Color code')

    def __str__(self) -> str:
        return self.title