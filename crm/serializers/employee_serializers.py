from rest_framework import serializers
from crm.models.employee import OrganizationEmployee
from crm.models.User import User


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