from crm.models.base_model import BaseModel
from crm.models.models import Bank, OrganizationAddress, Person
from crm.models.User import User
from helpers import enum
from django.core.validators import RegexValidator
from django.db import models


class Organization(BaseModel):
    logo = models.ImageField(
        verbose_name='Logo', upload_to='organization_logo', null=True)
    banner_image = models.ImageField(
        verbose_name='Banner image', upload_to='organization_banner', null=True)
    tint_color = models.CharField(verbose_name='Color', max_length=7, null=True, blank=True,
                                  validators=[RegexValidator(r'#[0-9A-Fa-f]{6}')])
    name = models.CharField(verbose_name='Name', max_length=128, unique=False, blank=False, null=True)
    legal_name = models.CharField(verbose_name='Legal name', max_length=512, blank=False, null=True)
    description = models.CharField(
        verbose_name='Description', max_length=2048, blank=False, null=True, default=None)
    address = models.ForeignKey(
        to=OrganizationAddress, on_delete=models.CASCADE, related_name='organizations', null=True)
    organization_type = models.PositiveSmallIntegerField(
        verbose_name='Organization type', choices=enum.OrganizationType.__list__, default=1)
    bank = models.ManyToManyField(
        Bank, verbose_name='Banks', related_name='organizations', blank=True)
    belongs_to = models.ForeignKey(Person, verbose_name='Director',
                                   related_name='companies', on_delete=models.SET_NULL, null=True, blank=True)

    def has_perm(self, user: User):
        return self.belongs_to == Person.objects.get(user=user)

    def __str__(self):
        return self.name
