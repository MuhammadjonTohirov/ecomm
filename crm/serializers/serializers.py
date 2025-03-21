from django.utils import timezone
from pyparsing import empty
from rest_framework import serializers
from rest_framework.fields import empty
from crm.models.organization import Organization
from crm.models.User import User
from crm.models.models import AppConfig, OrganizationAddress, Bank, Address, Person, Region
from crm.models.client import Client
from crm.models.employee import OrganizationEmployee
from utils.app_constants import ORGANIZATION_KEY

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_active']

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('cashback', 'balance', 'points')
        
class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.context['request'] = kwargs.get('context', None).get('request', None)
    
    class Meta:
        model = Person
        fields = ('id', 'user', 'is_business', 'avatar', 'phone_number', 'email', 'address')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        org_id = self.context.get(ORGANIZATION_KEY)
        if org_id:
            client = Client.objects.filter(user=instance, organization=org_id).first()
            if client is None:
                org = Organization.objects.get(id=org_id)
                client = Client.objects.create(user=instance, organization=org)
            
            data['account'] = ClientSerializer(client).data
        return data


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
        fields = ('id', 'name', 'description', 'logo', 'banner_image', 'tint_color',
                  'organization_type', 'bank', 'owner')

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

    def to_representation(self, instance: Organization):
        data = super().to_representation(instance)

        data['address'] = OrganizationAddressSerializer(
            instance.address, many=False).data
        return data


class OrganizationSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'logo', 'banner_image', 'tint_color',
                  'organization_type')
        
    def create(self, validated_data):
        raise NotImplementedError()

    def to_representation(self, instance: Organization):
        data = super().to_representation(instance)

        data['address'] = OrganizationAddressSerializer(
            instance.address, many=False).data
        return data


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class OrganizationEmployeeSerializer(serializers.ModelSerializer):
    roles_list = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    is_working_now = serializers.SerializerMethodField()
    
    class Meta:
        model = OrganizationEmployee
        fields = ['id', 'user', 'organization', 'assigned_stock_point', 
                  'roles_list', 'user_details', 'is_working_now']
    
    def get_roles_list(self, obj):
        return [{'id': role.id, 'title': role.title} for role in obj.roles.all()]
    
    def get_user_details(self, obj):
        try:
            user = User.objects.get(username=obj.user)
            return UserBasicSerializer(user).data
        except User.DoesNotExist:
            return None
    
    def get_is_working_now(self, obj):
        return obj.is_working()


class AppConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppConfig
        fields = '__all__'