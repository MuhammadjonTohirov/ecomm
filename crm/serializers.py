from django.utils import timezone
from rest_framework import serializers
from crm.models.organization import Organization
from crm.models.User import User

from crm.models.models import AppConfig, OrganizationAddress, Bank, Address, Region


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_active']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('street', 'location', 'zip_code')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['location'] = Region.objects.get(
            id=instance.location.id).__str__()
        return data


class OrganizationAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = OrganizationAddress
        fields = ('id', 'address', 'longitude', 'latitude')

    def to_representation(self, instance: OrganizationAddress):
        data: OrganizationAddress = super().to_representation(instance)
        data['address'] = f'{instance.building_number}, {Address.objects.get(id=instance.address.id).__str__()}'
        return data


class BankSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Bank
        fields = ('id', 'name', 'description', 'address',)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'logo', 'bannerImage', 'tint_color',
                  'organization_type', 'bank', 'belongs_to')

    def create(self, validated_data):
        name = validated_data.get('name')
        user = validated_data.user
        director = validated_data.get('director')
        description = validated_data.get('description')
        date = timezone.datetime.now()
        Organization.objects.create(name=name,
                                    created_date=date,
                                    created_by=user,
                                    description=description,
                                    bank_list=[], director=director)

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['address'] = OrganizationAddressSerializer(
            instance.organization_address, many=False).data
        return data


class AppConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppConfig
        fields = '__all__'
