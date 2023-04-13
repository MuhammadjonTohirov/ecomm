from django import forms

from django.http import HttpRequest
from pyparsing import Any
from crm.admin.base_admin_model import BaseAdminModel
from crm.helpers.organization_employee_helper import OrganizationEmployeeHelper
from crm.models.employee import OrganizationEmployee
from crm.models.employee_role import Role
from crm.models.organization import Organization
from crm.models.models import Person
from django.contrib import admin

from helpers.enum import CoreEmployeeType
from helpers.permissions import PermissionManager


class OrganizationAdminForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)

    def clean(self):
        return super().clean()


@admin.register(Organization)
class OrganizationAdmin(BaseAdminModel):
    form = OrganizationAdminForm
    list_display = ('legal_name', 'name', 'logo', 'banner_image',
                    'address', 'organization_type', 'owner')
    list_filter = ('name', 'organization_type',)
    search_fields = ('name',)
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'updated_date')

    fieldsets = [
        ('Basic Information', {'fields': [
         'name', 'legal_name', 'description', 'tint_color']}),
        ('Images', {'fields': ['logo', 'banner_image']}),
        ('Location', {'fields': ['address']}),
        ('Organization Type', {'fields': ['organization_type']}),
        ('Director Information', {'fields': ['owner']}),
        ('Financial Information', {'fields': ['bank']}),
    ] + BaseAdminModel.fieldsets

    filter_horizontal = ('bank',)

    # only superusers can delete organizations

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.owner == request.user or request.user.is_superuser:
            return True

        return super().has_change_permission(request, obj)

    # only company owner or superuser can get queryset
    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        self.request = request
        if request.user.is_superuser:
            return qs

        if (value := OrganizationEmployeeHelper.get_active_organizations(request.user)).exists():
            return value

        return OrganizationEmployeeHelper.get_active_organizations(request.user)

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user.is_superuser:
            return True

        if obj is None:
            return True

        return super().has_view_permission(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        # Assign default permissions to the user

        return super().response_add(request, obj, post_url_continue)

    # check that has permissions to add
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        person = Person.objects.filter(user=request.user).first()

        if person is None:
            return False
        
        if Organization.objects.filter(owner=person).count() >= 1:
            return False

        return person.is_business

    @staticmethod
    def get_organizations(request: HttpRequest):
        """_summary_
            Returns the organization that the user belongs to
        Returns:
            _type_: Organization
        """
        employees = OrganizationEmployee.objects.filter(
            user=request.user.username)

        organizations = Organization.objects.filter(
            id__in=employees.values_list('organization', flat=True))

        return organizations

    def save_form(self, request: Any, form: Any, change: Any) -> Any:
        return super().save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        result = super().save_model(request, obj, form, change)
        username = Person.objects.get(id=form['owner'].data).user.username
        OrganizationEmployeeHelper.create_employee(
            username=username,
            request=request,
            organization=obj,
            role=Role.objects.get(title=CoreEmployeeType.DIRECTOR.title))

        PermissionManager().defaultPermissionForBusinessUser(obj.owner.user.id)
        return result

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner' and not request.user.is_superuser:
            kwargs['queryset'] = Person.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
