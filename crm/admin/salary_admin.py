from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.db.models import Q

from crm.models.employee import OrganizationEmployee
from crm.models.organization import Organization
from crm.models.salary import EmployeeSalary, PaymentPeriod
from crm.admin.base_admin_model import BaseAdminModel
from crm.helpers.organization_employee_helper import OrganizationEmployeeHelper
from helpers.enum import Currency


class EmployeeSalaryForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(), 
        required=True,
        help_text="Select organization first to filter employees"
    )
    
    class Meta:
        model = EmployeeSalary
        fields = '__all__'
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Limit organizations based on user permissions
        if self.request and not self.request.user.is_superuser:
            # Get organizations where the user is an owner
            org_queryset = OrganizationEmployeeHelper.get_active_organizations(self.request.user)
            self.fields['organization'].queryset = org_queryset
        
        # Get the current employee if this is an existing instance
        current_employee = None
        if self.instance and self.instance.pk and hasattr(self.instance, 'employee'):
            current_employee = self.instance.employee
            
            try:
                # Get organization from employee
                org = current_employee.organization
                
                # Set initial value for organization
                self.initial['organization'] = org.pk
                
                # Make sure employee queryset includes the current employee
                self.fields['employee'].queryset = OrganizationEmployee.objects.filter(organization=org)
            except Exception as e:
                print(f"Error setting organization: {e}")
        
        # For form submissions, update the employee queryset based on selected organization
        if self.data and 'organization' in self.data:
            try:
                org_id = int(self.data.get('organization'))
                self.fields['employee'].queryset = OrganizationEmployee.objects.filter(organization_id=org_id)
            except (ValueError, TypeError):
                pass
        # If no organization selected yet but we have a current employee, ensure it's in the queryset
        elif current_employee:
            self.fields['employee'].queryset = OrganizationEmployee.objects.filter(pk=current_employee.pk)
        else:
            self.fields['employee'].queryset = OrganizationEmployee.objects.none()


@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(BaseAdminModel):
    form = EmployeeSalaryForm

    list_display = ('employee', 'amount_display', 'payment_period_display',
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
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/jquery.init.js',
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
        if db_field.name == "employee" and not request.user.is_superuser:
            # This will be filtered in the form based on selected organization
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def amount_display(self, obj):
        currency_map = {item[0]: item[1] for item in Currency.__list__}
        currency_label = currency_map.get(obj.currency, '')
        return f"{obj.amount} {currency_label}"
    amount_display.short_description = 'Amount'
    
    def payment_period_display(self, obj):
        return obj.get_payment_period_display()
    payment_period_display.short_description = 'Payment Period'
    
    def is_active_display(self, obj):
        is_active = obj.is_active()
        if is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    is_active_display.short_description = 'Active'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Get all organizations where the user is an owner or has relevant roles
        organizations = OrganizationEmployeeHelper.get_active_organizations(request.user)
        return qs.filter(employee__organization__in=organizations)
    
    def has_add_permission(self, request):
        # Anyone logged in should at least be able to see the model in admin
        return Organization.objects.filter(owner__user=request.user).exists()
        
    def has_change_permission(self, request, obj=None):
        # For permissions to view the module in admin
        if obj is None:
            return request.user.is_active
            
        # Superusers can change any salary
        if request.user.is_superuser:
            return True
            
        # Check if user owns the organization or has appropriate role
        is_owner = OrganizationEmployeeHelper.is_user_owner(request.user, obj.employee.organization)
        
        if is_owner:
            return True
            
        # Check if user has appropriate role in the organization
        has_role = OrganizationEmployee.objects.filter(
            user=request.user.username,
            organization=obj.employee.organization,
            roles__title__in=['DIRECTOR', 'MANAGER', 'HR', 'ACCOUNTANT']
        ).exists()
        
        return has_role and super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        # Similar logic to change permission
        if obj is None:
            return request.user.is_active
            
        return self.has_change_permission(request, obj)
    
    def has_view_permission(self, request, obj=None):
        # Anyone logged in should be able to see the model in admin
        return Organization.objects.filter(owner__user=request.user).exists()