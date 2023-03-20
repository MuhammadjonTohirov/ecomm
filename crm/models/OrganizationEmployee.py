from datetime import datetime
from django.dispatch import receiver
from crm.models.base_model import BaseModel
from django.db.models.signals import pre_save
from django.db import models

from crm.models.User import User


class OrganizationEmployee(BaseModel):
    user = models.CharField(max_length=255, blank=False, null=False,
                            default=None, db_index=True, verbose_name='Username')
    organization = models.ForeignKey('Organization',
                                     related_name='memberships', on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role')

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'organization')

    def user_object(self):
        return User.objects.get(username=self.user)

    def __str__(self):
        return f'{self.user_object().first_name} {self.user_object().last_name} in {self.organization.name}'

    def is_working(self):
        # if end_date is not set, then employee is working
        if self.end_date is None:
            return True
        
        if self.end_date > datetime.now().date():
            return True
        
        return False

    def roles_description(self) -> str:
        return ', '.join([role.title for role in self.roles.all()])


