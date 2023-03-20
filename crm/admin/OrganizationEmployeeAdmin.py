from django.utils.html import format_html
from django import forms
from django.http import HttpRequest
from pyparsing import Any
from crm.admin.base_admin_model import BaseAdminModel
from crm.models.organization import Organization
from crm.models.OrganizationEmployee import OrganizationEmployee
from crm.models.employee_role import Role
from crm.models.User import User
from crm.models.models import OrganizationEmployee, Person

from django.contrib import admin

from helpers.enum import CoreEmployeeType


@admin.register(Role)
class RoleAdmin(BaseAdminModel):
    list_display = ('title', 'description', 'created_date',
                    'updated_date', 'updated_by', 'created_by')
    fieldsets = [
        ('Role', {'fields': ['title', 'description']}),
    ] + BaseAdminModel.fieldsets
    
    def has_delete_permission(self, request, obj: Role=None):
        if obj is not None and obj.title in map(lambda x: x[1], CoreEmployeeType.__list__):
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        return self.has_delete_permission(request, obj)

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)
    
    def get_action(self, request):
        return super().get_action(request)
    
    class Media:
        css = {
            'all': ('assets/css/admin_custom.css',),
        }


class OrganizationEmployeeForm(forms.ModelForm):
    class Meta:
        model = OrganizationEmployee
        fields = '__all__'

    def clean_user(self):
        username = self.cleaned_data.get('user', None)
        if username is None:
            raise forms.ValidationError("There is no user with such username.")

        if User.objects.filter(username=username).exists():
            return username
        raise forms.ValidationError("User with such username does not exist.")


@admin.register(OrganizationEmployee)
class OrganizationEmployeeAdmin(BaseAdminModel):
    form = OrganizationEmployeeForm
    list_display = ('user_object', 'organization', 'roles_description',
                    'start_date', 'end_date', 'is_working')
    search_fields = ('user', 'organization__name')
    list_filter = ['start_date', 'end_date']

    fieldsets = [('Organization Employee', {'fields': [
                  'user', 'organization', 'roles', 'start_date', 'end_date']})] + BaseAdminModel.fieldsets

    filter_horizontal = ('roles',)

    def is_working(self, obj: OrganizationEmployee):
        return obj.is_working()

    def user_object(self, obj):
        user = User.objects.get(username=obj.user)
        return f'{user.first_name} {user.last_name}'

    # show employees of the organization
    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(organization__belongs_to__user=request.user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "organization":
                kwargs["queryset"] = Organization.objects.filter(
                    belongs_to__user=request.user.id)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def delete_model(self, request, obj: OrganizationEmployee):
        if obj.organization.belongs_to is None:
            return super().delete_model(request, obj)
        if obj.organization.belongs_to.user == obj.user_object():
            organization = obj.organization
            if isinstance(organization, Organization):
                organization.belongs_to = None
                organization.save()

        return super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

    def save_model(self, request, obj, form, change):
        if obj is None:
            return
        return super().save_model(request, obj, form, change)

    @staticmethod
    def works_in_organization(cls, user: User, organization: Organization):
        return OrganizationEmployee.objects.filter(user=user.username, organization=organization).exists()

    @staticmethod
    def get_organizations(user: User) -> list:
        """_summary_
        Returns list of organizations where user works.
        """
        return OrganizationEmployee.objects.filter(user=user.username).values_list('organization', flat=True)
