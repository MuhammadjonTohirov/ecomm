from datetime import datetime
from crm.models.organization import Organization
from crm.models.User import User
from crm.models.employee_role import Role

from crm.models.models import *
from helpers.enum import CoreEmployeeType
from wms.models.product_unit import ProductUnit
from wms.models.field_type import FieldType
from wms.models.product_category import ProductCategory
from wms.models import *


class CrmDefaults:
    @classmethod
    def init_banks(cls, request):
        try:
            address = Address.objects.first()
            user = request.user
            Bank.objects.update_or_create(id=1, defaults={
                'name': 'Kaptial bank',
                'address': address,
                'description': 'This is auto generated bank item',
                'created_by': user,
                'created_date': datetime.now()
            })
            return True
        except Exception as ex:
            print(ex.__str__())
            return False


class Defaults:
    @classmethod
    def init_countries(cls):
        Country.objects.update_or_create(title='Uzbekistan', defaults={
            'description': 'Uzbekistan is located in the Central Asia'
        })

    @classmethod
    def init_provinces(cls):
        Province.objects.update_or_create(title='Fergana', defaults={
            'description': 'Fergana is the most beautiful province of Uzbekistan',
            'country': Country.objects.get(title='Uzbekistan')
        })

    @classmethod
    def init_regions(cls):
        Region.objects.update_or_create(title='Fergana city', defaults={
            'description': 'Fergana city',
            'province': Province.objects.get(title='Fergana')
        })

    @classmethod
    def init_roles(cls):
        accountant = CoreEmployeeType.ACCOUNTANT
        director = CoreEmployeeType.DIRECTOR
        manager = CoreEmployeeType.MANAGER
        
        Role.objects.update_or_create(title=manager[1], defaults={
            'description': 'Manager role',
        })

        Role.objects.update_or_create(title=accountant[1], defaults={
            'description': 'Accountant role',
        })
        
        Role.objects.update_or_create(title=director[1], defaults={
            'description': 'Director role',
        })

    @classmethod
    def init_addresses(cls):
        Address.objects.update_or_create(zip_code=1212, defaults={
            'id': 1,
            'street': 'Alisher Navoiy',
            'location': Region.objects.get(title='Fergana city')
        })

        Address.objects.update_or_create(zip_code=1212, defaults={
            'id': 2,
            'street': 'Obod Turmush',
            'location': Region.objects.get(title='Fergana city')
        })

        OrganizationAddress.objects.update_or_create(
            id=1, defaults={
                'building_number': 32,
                'address_id': 1,
                'longitude': 71.721951,
                'latitude': 40.378130
            }
        )

        OrganizationAddress.objects.update_or_create(
            id=2, defaults={
                'building_number': 104,
                'address_id': 2,
                'longitude': 71.781536,
                'latitude': 40.365119
            }
        )

    @classmethod
    def init_product_units(cls):
        ProductUnit.objects.update_or_create(title='kg', defaults={
            'description': 'Kilo Gram'
        })

        ProductUnit.objects.update_or_create(title='gr', defaults={
            'description': 'Gram'
        })

        ProductUnit.objects.update_or_create(title='m', defaults={
            'description': 'Meter'
        })

        ProductUnit.objects.update_or_create(title='sm', defaults={
            'description': 'Santi meter'
        })

        ProductUnit.objects.update_or_create(title='Bag', defaults={
            'description': 'Bag, Sac'
        })

        ProductUnit.objects.update_or_create(title='Box', defaults={
            'description': ''
        })

        ProductUnit.objects.update_or_create(title='Block', defaults={
            'description': ''
        })

        ProductUnit.objects.update_or_create(title='Piece', defaults={

        })

    @classmethod
    def init_product_categories(cls):
        if not ProductCategory.objects.filter(title='Food').exists():
            ProductCategory.objects.create(title='Food', description='Food')

        if not ProductCategory.objects.filter(title='Clothes').exists():
            ProductCategory.objects.update_or_create(title='Clothes', defaults={
                'description': 'Clothes, Shoes, etc.'
            })

        if not ProductCategory.objects.filter(title='Cosmetics').exists():
            ProductCategory.objects.update_or_create(title='Cosmetics', defaults={
                'description': ''
            })

    @classmethod
    def init_field_types(cls):
        FieldType.objects.update_or_create(title='Decimal')
        FieldType.objects.update_or_create(title='Currency')
        FieldType.objects.update_or_create(title='Text')
        FieldType.objects.update_or_create(title='Email')

    @classmethod
    def init_persons(cls):
        if User.objects.first() is not None:
            Person.objects.update_or_create(id=1, user=User.objects.first())

        if User.objects.last() is not None:
            Person.objects.update_or_create(id=2, user=User.objects.last())

    @classmethod
    def init_organizations(cls):

        Organization.objects.update_or_create(
            id=1,
            name='City Food',
            defaults={
                'organization_address': OrganizationAddress.objects.first, 'organization_type': 1
            }
        )

        Organization.objects.update_or_create(
            id=2,
            name='Electronic Arts',
            defaults={
                'organization_address': OrganizationAddress.objects.last(), 'organization_type': 1
            }
        )

    @classmethod
    def deploy(cls):
        try:
            if not Country.objects.exists():
                Defaults.init_countries()

            if not Province.objects.exists():
                Defaults.init_provinces()

            if not Region.objects.exists():
                Defaults.init_regions()

            if not Address.objects.exists():
                Defaults.init_addresses()

            if not ProductUnit.objects.exists():
                Defaults.init_product_units()

            if not ProductCategory.objects.exists():
                Defaults.init_product_categories()

            if not FieldType.objects.exists():
                Defaults.init_field_types()

            if not Person.objects.exists():
                Defaults.init_persons()

            if not Organization.objects.exists():
                Defaults.init_organizations()

            Defaults.init_roles()

        except Exception as e:
            print(e.__str__())
