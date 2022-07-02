from datetime import datetime

from crm.models import *
from helpers.responses import AppResponse
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
    def init_addresses(cls):
        Address.objects.update_or_create(zip_code=1212, defaults={
            'id': 1,
            'street': 'Alisher Navoiy',
            'location': Region.objects.get(title='Fergana city')
        })

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
        ProductCategory.objects.update_or_create(title='Food', defaults={
            'description': ''
        })

        ProductCategory.objects.update_or_create(title='Clothes', defaults={
            'description': 'Clothes, Shoes, etc.'
        })

        ProductCategory.objects.update_or_create(title='Cosmetics', defaults={
            'description': ''
        })

    @classmethod
    def deploy(cls):
        try:
            Defaults.init_countries()
            Defaults.init_provinces()
            Defaults.init_regions()
            Defaults.init_addresses()
            Defaults.init_product_units()
            Defaults.init_product_categories()
        except Exception as e:
            print(e.__str__())
