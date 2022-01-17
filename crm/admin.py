from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from crm.models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'belongs_to', 'created_date')


admin.site.register(Person)


# class IndividualPersonAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_date')


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_date')
