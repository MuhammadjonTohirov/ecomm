
from crm.models.base_model import BaseModel
from django.db import models

from crm.models.models import Person

class Client(BaseModel):
    card_number = models.CharField(max_length=20, unique=False, null=True, blank=False)
    user = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True)
    cashback = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.user.user.username} {self.created_date}'
    
    class Meta:
        # unique user with organization
        unique_together = ('user', 'organization')
        