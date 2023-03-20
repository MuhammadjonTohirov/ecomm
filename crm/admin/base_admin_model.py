from crm.models.models import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone

class BaseAdminModel(admin.ModelAdmin):
    fieldsets = [
        (_('Created/Updated meta'), {'fields': ('created_date', 'updated_date'), 'classes': ('collapse',)}),
    ]
    
    def has_add_permission(self, request):
        """
        Disable the ability to add new instances of this model.
        """
        return request.user.is_active and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Disable the ability to delete instances of this model.
        """
        return request.user.is_active and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and super().has_add_permission(request)

    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_date = datetime.now(timezone.utc)
        else:
            obj.updated_date = datetime.now(timezone.utc)

        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            created_by_username=models.F('created_by__username'),
            updated_by_username=models.F('updated_by__username'),
        )
