from django.db import models
from crm.models.base_model import BaseModel
from crm.models.models import Person
from crm.models.organization import Organization


class CustomerCard(BaseModel):
    user = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True)
    is_active = models.BooleanField(default=True)
    card_number = models.CharField(
        max_length=255, null=True, default=None, blank=False)
    by_organization = models.ForeignKey(
        Organization, on_delete=models.DO_NOTHING, null=True)
    points = models.IntegerField(default=0)
    deposit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_spent = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.user.username} {self.created_date}'
