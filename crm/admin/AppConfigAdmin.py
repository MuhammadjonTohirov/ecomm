from crm.models.models import AppConfig


from django.contrib import admin


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    model = AppConfig
    list_display = ('version', 'is_active')