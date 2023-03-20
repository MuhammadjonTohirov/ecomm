from crm.admin.base_admin_model import BaseAdminModel
from crm.models.User import User
from wms.models.Color import Color


from django.contrib import admin


@admin.register(Color)
class ColorAdmin(BaseAdminModel):
    model = Color
    list_display = ('id', 'title', 'code', 'created_date',
                    'updated_date', 'created_by', 'updated_by')

    fieldsets = [
        (('Color'), {'fields': ('title', 'code')}),
    ] + BaseAdminModel.fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        superusers = User.objects.filter(is_superuser=True)
        supers_array = list(superusers)
        supers_array.append(request.user)
        return qs.filter(created_by__in=supers_array)
