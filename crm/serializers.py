from django.utils import timezone
from rest_framework import serializers

from crm.models import Profile, Bank, Address, Organization, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_active']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Bank
        fields = ('id', 'name', 'description', 'address',)


class OrganizationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Organization
        fields = ('name', 'description', 'address', 'organization_type', 'bank', 'belongs_to')

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

        # Profile.objects.create(user=user, **profile_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    # position_name = serializers.CharField(source="position")
    # is_active = serializers.BooleanField(source="user.is_active")
    # is_superuser = serializers.BooleanField(source="user.is_superuser")
    # last_login = serializers.DateTimeField(source="user.last_login", format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Profile
        fields = ('id',
                  'first_name',
                  'last_name', 'email')
        # 'email',
        # 'position_name',
        # 'middle_name',
        # 'is_active',
        # 'is_superuser',
        # 'last_login')
