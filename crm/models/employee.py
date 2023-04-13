from django.db.models import Q
from datetime import datetime
from django.dispatch import receiver
from crm.models.base_model import BaseModel
from django.db.models.signals import pre_save
from django.db import models

from crm.models.User import User
from crm.models.employee_role import Role
from crm.models.models import Person
from helpers.enum import CoreEmployeeType


class OrganizationEmployee(BaseModel):
    user = models.CharField(max_length=255, blank=False, null=False,
                            default=None, db_index=True, verbose_name='Username')
    organization = models.ForeignKey('Organization',
                                     related_name='memberships', on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role')

    class Meta:
        unique_together = ('user', 'organization')

    def user_object(self):
        return User.objects.get(username=self.user)

    def __str__(self):
        return f'{self.user_object().first_name} {self.user_object().last_name} in {self.organization.name}'

    def is_working(self):
        person = Person.objects.get(user__username=self.user)
        return EmployeeCareerLog.objects.filter(person=person, is_working=True).exists()

    def roles_description(self) -> str:
        return ', '.join([role.title for role in self.roles.all()])

    def is_director(self):
        return self.roles.filter(title=CoreEmployeeType.DIRECTOR.title).exists()

    def save(self, *args, **kwargs):
        if self.id is None:
            # on create new employee
            EmployeeCareerLog.objects.create(person=Person.objects.get(user__username=self.user),
                                             organization=self.organization,
                                             start_date=datetime.now(), is_working=True)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        EmployeeCareerLog.objects.filter(
            person=Person.objects.get(user__username=self.user),
            organization=self.organization,
            is_working=True
        ).update(is_working=False, end_date=datetime.now())
        super().delete(*args, **kwargs)


class EmployeeCareerLog(BaseModel):
    person = models.ForeignKey(
        'Person', related_name='career_log', on_delete=models.CASCADE, null=True, blank=False, default=None)
    organization = models.ForeignKey(
        'Organization', related_name='career_log', on_delete=models.CASCADE, null=True, blank=False, default=None)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_working = models.BooleanField(default=True)
