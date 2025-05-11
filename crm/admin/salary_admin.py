from django.contrib import admin
from django.utils.html import format_html
from crm.forms.employee_saray_form import EmployeeSalaryForm
from crm.models.employee import OrganizationEmployee
from crm.models.salary import EmployeeSalary, PaymentPeriod
from crm.admin.base_admin_model import BaseAdminModel


@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(BaseAdminModel):
    form = EmployeeSalaryForm

    list_display = ('employee', 'amount', 'currency_display', 'payment_period_display',
                    'start_date', 'end_date', 'is_active_display', 'bonus_eligible')
    list_filter = ('payment_period', 'currency', 'bonus_eligible', 'start_date')
    search_fields = ('employee__user', 'notes')
    date_hierarchy = 'start_date'
    
    fieldsets = [
        ('Salary Information', {
            'fields': ['organization', 'employee', 'amount', 'currency', 'payment_period']
        }),
        ('Period', {
            'fields': ['start_date', 'end_date', 'bonus_eligible']
        }),
        ('Additional Information', {
            'fields': ['notes']
        }),
    ] + BaseAdminModel.fieldsets
    
    class Media:
        js = (
            '/admin/js/vendor/jquery/jquery.min.js',
            '/admin/js/jquery.init.js',
            'js/employee_salary_form.js',
            )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Pass the request to the form
        class FormWithRequest(form):
            def __init__(self, *args, **inner_kwargs):
                inner_kwargs['request'] = request
                super().__init__(*args, **inner_kwargs)
        return FormWithRequest
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            if request.user.is_superuser:
                kwargs["queryset"] = OrganizationEmployee.objects.all()
            else:
                kwargs["queryset"] = OrganizationEmployee.objects.filter(organization__owner__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_view_permission(self, request, obj = ...):
        return request.user.is_active
    
    def has_change_permission(self, request, obj = ...):
        return request.user.is_active
    
    def has_add_permission(self, request):
        return request.user.is_active
    
    def currency_display(self, obj):
        currency_map = {1: 'Sum', 2: 'Dollar', 3: 'Euro'}
        return currency_map.get(obj.currency, 'Unknown')
    currency_display.short_description = 'Currency'
    
    def payment_period_display(self, obj):
        return obj.get_payment_period_display()
    payment_period_display.short_description = 'Payment Period'
    
    def is_active_display(self, obj):
        is_active = obj.is_active()
        if is_active:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    is_active_display.short_description = 'Active'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter to only show salaries for employees in organizations the user has access to
        return qs.filter(employee__organization__owner__user=request.user)
    

