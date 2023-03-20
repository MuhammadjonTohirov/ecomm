from datetime import datetime

from django.http import HttpRequest
from crm.admin.OrganizationEmployeeAdmin import OrganizationEmployeeAdmin
from crm.admin.base_admin_model import BaseAdminModel
from crm.models.organization import Organization
from crm.models.models import Person
from django.contrib import admin


@admin.register(Organization)
class OrganizationAdmin(BaseAdminModel):
    list_display = ('legal_name', 'name', 'logo', 'banner_image', 'tint_color',
                    'description', 'address', 'organization_type', 'belongs_to')
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
        ('Director Information', {'fields': ['belongs_to']}),
        ('Financial Information', {'fields': ['bank']}),
    ] + BaseAdminModel.fieldsets

    filter_horizontal = ('bank',)

    # only superusers can delete organizations
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # only company owner or superuser can get queryset
    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        if (value := self.get_organization(request)).exists():
            return value
        
        return qs.filter(id__in=OrganizationEmployeeAdmin.get_organizations(request.user))

    def has_view_permission(self, request, obj = None) -> bool:
        if request.user.is_superuser:
            return True
        
        if obj is None:
            return True
        
        person = Person.objects.get(user=request.user)
        return obj.belongs_to == person or super().has_view_permission(request, obj)

    # only company owner or superuser can edit
    # def has_change_permission(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     if obj is None:
    #         return True

    #     # check if the user has change permission on the organization
    #     has_change_permission = ModelPermission(
    #         request.user.id).has_change_permission(Organization)
    #     person = Person.objects.get(user=request.user)
    #     return obj.belongs_to == person or has_change_permission

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

        has_organization = Organization.objects.filter(
            belongs_to=person
        ).exists()

        return person.is_business and not has_organization

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'belongs_to':
                kwargs["queryset"] = Person.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    @staticmethod
    def get_organization(request) -> Organization:
        """_summary_
            Returns the organization that the user belongs to
        Returns:
            _type_: Organization
        """     
        person = Person.objects.filter(user=request.user).first()
        return Organization.objects.filter(belongs_to=person)