from crm.models.base_model import BaseModel
from crm.models.User import User 


from django.db import models


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} {self.created_date}'
