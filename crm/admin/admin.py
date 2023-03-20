from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from crm.models.User import User
from crm.models.User import User
from crm.models.OrganizationEmployee import OrganizationEmployee

from crm.models.models import *

admin.site.site_header = "Admin panel"

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {
            # permissons to models
            'classes': ('collapse',),
            'description': 'Permissions to models',
            # 'groups',
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        # (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    # Override response_add method to conditionaly assign permission
    def response_add(self, request, obj, post_url_continue=None):
        return super().response_add(request, obj, post_url_continue)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        Person.objects.get_or_create(user=obj)


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'id', 'location', 'zip_code',
                    'created_date', 'updated_date', 'created_by', 'updated_by')

    fieldsets = [('Address', {'fields': ['street', 'location', 'zip_code']})]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        obj.save()


@admin.register(OrganizationAddress)
class OrganizationAddressAdmin(admin.ModelAdmin):
    list_display = ('building_number', 'id',
                    'address', 'latitude', 'longitude')


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description', 'created_date')


@admin.register(Province)
@admin.register(Region)
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'description')


class EmployeeInline(admin.TabularInline):
    # list_display = ('id', 'user', 'organization', 'start_date', 'end_date')
    # search_fields = ('user__first_name', 'user__last_name', 'user__email',
    #                  'organization__name')
    # list_filter = ('organization__name',)
    model = OrganizationEmployee
    extra = 0

