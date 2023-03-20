from django.db import models

from crm.models.base_model import BaseModel


class OrderState(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title