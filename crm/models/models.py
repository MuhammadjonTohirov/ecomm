from django.db import models
from crm.models.base_model import BaseModel
from crm.models.OrganizationEmployee import OrganizationEmployee
from crm.models.User import User

from helpers import enum


class AppConfig(models.Model):
    version = models.SmallIntegerField(default=1, unique=True)
    is_active = models.BooleanField(default=True)
    tint_color = models.CharField(max_length=7, default='#000000')
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#000000')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='app_config_created_by', null=True, blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='app_config_updated_by', null=True, blank=True)

    @classmethod
    def create(cls, version, is_active, tint_color, background_color, text_color, created_by, updated_by):
        return cls.objects.create(
            version=version,
            is_active=is_active,
            tint_color=tint_color,
            background_color=background_color,
            text_color=text_color,
            created_by=created_by,
            updated_by=updated_by,
        )


class Country(models.Model):
    title = models.CharField(verbose_name='Country name',
                             max_length=128, unique=True)
    description = models.CharField(verbose_name='Description', max_length=1024)

    def __str__(self):
        return self.title


class Province(models.Model):
    country = models.OneToOneField(to=Country, verbose_name='Country', on_delete=models.CASCADE, null=True, blank=True,
                                   default=None, unique=True)
    title = models.CharField(verbose_name='Province name', max_length=128)
    description = models.CharField(verbose_name='Description', max_length=1024)

    def __str__(self):
        return self.title


class Region(models.Model):
    province = models.OneToOneField(to=Province, verbose_name='Province', on_delete=models.CASCADE, null=True, blank=True,
                                    default=None)
    title = models.CharField(
        verbose_name='Region/City name', max_length=128, unique=True)
    description = models.CharField(verbose_name='Description', max_length=1024)

    def __str__(self):
        return f'{self.title}, {self.province}, {self.province.country}'


class Address(BaseModel):
    street = models.CharField(verbose_name='Street', max_length=128)
    location = models.ForeignKey(to=Region, verbose_name='Region', on_delete=models.SET_NULL, null=True,
                                 default=None, blank=True)

    zip_code = models.PositiveIntegerField(verbose_name='Zip code')

    def __str__(self):
        return f'{self.street}, {self.location}, {self.zip_code}'


class OrganizationAddress(models.Model):
    building_number = models.CharField(
        verbose_name='Building number', max_length=128,)
    address = models.ForeignKey(to=Address, verbose_name='Address', on_delete=models.CASCADE, null=True, blank=True,
                                default=None)
    longitude = models.FloatField(
        verbose_name='Longitude', blank=True, null=True,)
    latitude = models.FloatField(
        verbose_name='Latitude', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.building_number} {self.address}'

    class Meta:
        unique_together = ('latitude', 'longitude')
        verbose_name_plural = 'Organization addresses'
        verbose_name = 'Organization address'


class Bank(models.Model):
    name = models.CharField(verbose_name='Bank name', max_length=256)
    description = models.CharField(verbose_name='Description', max_length=1024)
    address = models.ForeignKey(to=Address, on_delete=models.SET_NULL, default=None, blank=False, null=True,
                                related_name='bank_address')
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(
        verbose_name='Updated date', blank=True, null=True)

    created_by = models.OneToOneField(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                      related_name='bank_created_by')

    updated_by = models.OneToOneField(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                      related_name='bank_updated_by')

    def __str__(self):
        return f'{self.name} {self.address}'


class Person(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User',
                                related_name='person_user', null=True, blank=True, default=None, unique=True)
    is_business = models.BooleanField(
        verbose_name='Is business', default=False)

    def __str__(self):
        return f'{self.user.__str__()} {self.user.first_name} {self.user.last_name}'


class File(models.Model):
    name = models.CharField(verbose_name='File name', max_length=512)
    file = models.FileField(verbose_name='File', null=False, default=None)

    created_date = models.DateTimeField(
        verbose_name='Created date', auto_created=True, auto_now=True, blank=True)

    updated_date = models.DateTimeField(
        verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='file_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='file_updated_by')
