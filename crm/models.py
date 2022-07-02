from django.contrib.auth.models import AbstractUser
from django.db import models

from helpers import enum


class User(AbstractUser):
    pass


class Country(models.Model):
    title = models.CharField(verbose_name='Country name', max_length=128, unique=True)
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
    title = models.CharField(verbose_name='Region/City name', max_length=128, unique=True)
    description = models.CharField(verbose_name='Description', max_length=1024)

    def __str__(self):
        return f'{self.title}, {self.province}, {self.province.country}'


class Address(models.Model):
    street = models.CharField(verbose_name='Street', max_length=128)
    location = models.ForeignKey(to=Region, verbose_name='Region', on_delete=models.SET_NULL, null=True,
                                    default=None, blank=True)

    zip_code = models.PositiveIntegerField(verbose_name='Zip code')

    def __str__(self):
        return f'{self.street}, {self.location}'


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='User', related_name='profile_user')
    birth_date = models.DateField(verbose_name='Birth date', blank=True, null=True)
    gender = models.SmallIntegerField(verbose_name='Gender', choices=enum.Gender.__list__, null=False, default=1,
                                      blank=True)
    address = models.OneToOneField(to=Address, verbose_name='Address', on_delete=models.SET_NULL, default=None,
                                   blank=True, null=True)

    organization = models.ForeignKey(to='Organization', verbose_name='Works in', blank=True, null=True,
                                     related_name='profile_organization', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} details'


class Bank(models.Model):
    name = models.CharField(verbose_name='Bank name', max_length=256)
    description = models.CharField(verbose_name='Description', max_length=1024)
    address = models.ForeignKey(to=Address, on_delete=models.SET_NULL, default=None, blank=False, null=True,
                                related_name='bank_address')
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.OneToOneField(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                      related_name='bank_created_by')

    updated_by = models.OneToOneField(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                      related_name='bank_updated_by')

    def __str__(self):
        return f'{self.name} {self.address}'


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User',
                                related_name='person_user', null=True, blank=True, default=None, unique=True)

    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True,
                                        blank=True)
    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='p_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='p_updated_by')

    def __str__(self):
        return f'{self.user.__str__()} {self.user.first_name} {self.user.last_name}'


class Organization(models.Model):
    logo = models.ImageField(verbose_name='Logo', upload_to='organization_logo', blank=False, null=True)
    name = models.CharField(verbose_name='name', max_length=512, default=None, null=True, blank=False, unique=True)
    description = models.CharField(verbose_name='Description', max_length=2048, default=None, null=True, blank=False)
    address = models.ForeignKey(to=Address, on_delete=models.SET_NULL, default=None, blank=True, null=True,)
    organization_type = models.SmallIntegerField(verbose_name='Organization type', choices=enum.OrganizationType.__list__, null=False, default=1, blank=True) 
    bank = models.ManyToManyField(Bank, verbose_name='Bank list', related_name='company_bank_list', default=None, blank=True)
    belongs_to = models.ForeignKey(Person, verbose_name='Director', related_name='company_director', on_delete=models.CASCADE, null=True, blank=True, default=None)
    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True, blank=True)
    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='company_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='company_updated_by')

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(verbose_name='File name', max_length=512)
    file = models.FileField(verbose_name='File', null=False, default=None)

    created_date = models.DateTimeField(verbose_name='Created date', auto_created=True, auto_now=True, blank=True)

    updated_date = models.DateTimeField(verbose_name='Updated date', blank=True, null=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='file_created_by')

    updated_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, default=None, null=True,
                                   related_name='file_updated_by')
