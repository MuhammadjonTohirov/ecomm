from django.contrib import messages
from django.db.models import Q
from django import forms
from django.http import HttpRequest
from crm.admin.base_admin_model import BaseAdminModel
from crm.helpers.organization_employee_helper import OrganizationEmployeeHelper
from crm.models.employee import EmployeeCareerLog, OrganizationEmployee
from crm.models.employee_role import Role
from crm.models.User import User

from django.contrib import admin

from helpers.enum import CoreEmployeeType


@admin.register(Role)
class RoleAdmin(BaseAdminModel):
    list_display = ('title', 'description', 'created_date',
                    'updated_date', 'updated_by', 'created_by')
    fieldsets = [
        ('Role', {'fields': ['title', 'description']}),
    ] + BaseAdminModel.fieldsets

    def has_change_permission(self, request, obj=None):
        if (obj is not None and obj.title in obj.title in CoreEmployeeType.__list__ and obj.created_by != request.user) and not request.user.is_superuser:
            return False

        return self.has_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if (obj is not None and obj.title in obj.title in CoreEmployeeType.__list__ and obj.created_by != request.user) and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if (obj is not None and obj.title in obj.title in CoreEmployeeType.__list__ and obj.created_by != request.user) and not request.user.is_superuser:
                messages.add_message(request, messages.ERROR, (
                    "Widget #1 is protected, please remove it from your selection "
                    "and try again."
                ))
                return
        super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        self.request = request
        if request.user.is_superuser:
            return super().get_queryset(request)
        return super().get_queryset(request).filter(created_by=request.user)

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
    list_display = ('user_object', 'organization', 'assigned_stock_point',
                    'roles_description')
    search_fields = ('user', 'organization__name')

    fieldsets = [('Organization Employee', {'fields': [
                  'user', 'organization', 'assigned_stock_point', 'roles']})] + BaseAdminModel.fieldsets

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

        return qs.filter(organization__in=OrganizationEmployeeHelper.get_active_organizations(request.user))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "organization":
                kwargs["queryset"] = OrganizationEmployeeHelper.get_active_organizations(
                    request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and (CoreEmployeeType.DIRECTOR.title in obj.roles.values_list('title', flat=True)):
            return False

        return super().has_delete_permission(request, obj)

    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj is not None and OrganizationEmployeeHelper.is_user_owner(request.user, obj.organization):
            return True

        if obj is not None:
            roles = obj.roles.values_list('title', flat=True)
            if CoreEmployeeType.MANAGER.title in roles or\
                CoreEmployeeType.ACCOUNTANT.title in roles or\
                    CoreEmployeeType.HR.title in roles or\
            CoreEmployeeType.DIRECTOR.title in roles:
                return False

        return super().has_change_permission(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

    def create_model(self, request, obj: OrganizationEmployee, form, change):
        pass

    def save_model(self, request, obj: OrganizationEmployee, form, change):
        if obj is None:
            return

        return super().save_model(request, obj, form, change)


@admin.register(EmployeeCareerLog)
class EmployeeCareerLogAdmin(BaseAdminModel):
    list_display = ('person', 'organization',
                    'start_date', 'end_date', 'is_working')
    fieldsets = [('Employee Career Log', {'fields': [
                  'person', 'organization', 'start_date', 'end_date', 'is_working']})] + BaseAdminModel.fieldsets

    def has_change_permission(self, request, obj=None):
        return False  # or request.user.is_superuser

    def has_add_permission(self, request):
        return False  # or request.user.is_superuser

    def get_queryset(self, request):
        if not request.user.is_superuser:
            organizations = OrganizationEmployee.objects.filter(
                user=request.user.username).values_list('organization', flat=True)
            return EmployeeCareerLog.objects.filter(organization__in=organizations)
        return super().get_queryset(request)
