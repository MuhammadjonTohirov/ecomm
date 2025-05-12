from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.db.models import Q
from django.utils import timezone

from crm.models.attendance import AttendanceStatus, EmployeeAttendance
from crm.models.employee import OrganizationEmployee
from crm.models.organization import Organization
from crm.admin.base_admin_model import BaseAdminModel
from crm.helpers.organization_employee_helper import OrganizationEmployeeHelper


class EmployeeAttendanceForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(), 
        required=True,
        help_text="Select organization first to filter employees"
    )
    
    class Meta:
        model = EmployeeAttendance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Make working_hours read-only
        if 'working_hours' in self.fields:
            self.fields['working_hours'].widget.attrs['readonly'] = True
        
        # Limit organizations based on user permissions
        if self.request and not self.request.user.is_superuser:
            org_queryset = OrganizationEmployeeHelper.get_active_organizations(self.request.user)
            self.fields['organization'].queryset = org_queryset
        
        # Get the current employee if this is an existing instance
        current_employee = None
        if self.instance and self.instance.pk and hasattr(self.instance, 'employee'):
            current_employee = self.instance.employee
            current_org = self.instance.organization
            
            # Set initial value for organization
            self.initial['organization'] = current_org.pk
            
            # Make sure employee queryset includes the current employee
            self.fields['employee'].queryset = OrganizationEmployee.objects.filter(organization=current_org)
        
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


@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(BaseAdminModel):
    form = EmployeeAttendanceForm
    
    list_display = ('employee', 'date', 'status_display', 'check_in_time_display',
                    'check_out_time_display', 'working_hours', 'location')
    list_filter = ('status', 'date', 'organization')
    search_fields = ('employee__user', 'notes', 'location')
    date_hierarchy = 'date'
    
    fieldsets = [
        ('Employee Information', {
            'fields': ['organization', 'employee']
        }),
        ('Attendance Details', {
            'fields': ['date', 'check_in_time', 'check_out_time', 'status', 'working_hours']
        }),
        ('Additional Information', {
            'fields': ['location', 'notes']
        }),
    ] + BaseAdminModel.fieldsets
    
    readonly_fields = ('working_hours',)
    
    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/jquery.init.js',
            'js/employee_attendance_form.js',
        )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Pass the request to the form
        class FormWithRequest(form):
            def __init__(self, *args, **inner_kwargs):
                inner_kwargs['request'] = request
                super().__init__(*args, **inner_kwargs)
        return FormWithRequest
    
    def status_display(self, obj):
        status_colors = {
            AttendanceStatus.PRESENT: 'green',
            AttendanceStatus.LATE: 'orange',
            AttendanceStatus.HALF_DAY: 'blue',
            AttendanceStatus.ABSENT: 'red',
            AttendanceStatus.ON_LEAVE: 'purple'
        }
        color = status_colors.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 
                          color, obj.get_status_display())
    status_display.short_description = 'Status'
    
    def check_in_time_display(self, obj):
        if obj.check_in_time:
            return obj.check_in_time.strftime('%H:%M:%S')
        return '-'
    check_in_time_display.short_description = 'Check In'
    
    def check_out_time_display(self, obj):
        if obj.check_out_time:
            return obj.check_out_time.strftime('%H:%M:%S')
        return '-'
    check_out_time_display.short_description = 'Check Out'
    
    def save_model(self, request, obj, form, change):
        # Auto-calculate working hours if both check-in and check-out are provided
        if obj.check_in_time and obj.check_out_time:
            delta = obj.check_out_time - obj.check_in_time
            obj.working_hours = round(delta.total_seconds() / 3600, 2)
            
            # Auto-determine status based on working hours and check-in time
            # This can be customized according to your business rules
            if obj.working_hours < 4:
                obj.status = AttendanceStatus.HALF_DAY
            elif obj.check_in_time.time() > timezone.datetime.strptime('09:30', '%H:%M').time():
                obj.status = AttendanceStatus.LATE
            else:
                obj.status = AttendanceStatus.PRESENT
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Get all organizations where the user is an owner or has relevant roles
        organizations = OrganizationEmployeeHelper.get_active_organizations(request.user)
        return qs.filter(organization__in=organizations)
    
    def has_add_permission(self, request):
        # Superusers and users with appropriate roles can add attendance records
        if request.user.is_superuser:
            return True
        
        # Check if user is an owner or has a management role in any organization
        has_permission = OrganizationEmployee.objects.filter(
            user=request.user.username,
            roles__title__in=['DIRECTOR', 'MANAGER', 'HR']
        ).exists() or Organization.objects.filter(owner__user=request.user).exists()
        
        return has_permission
    
    def has_change_permission(self, request, obj=None):
        # Superusers can change any attendance record
        if request.user.is_superuser:
            return True
            
        # If we don't have a specific object, check general permission
        if obj is None:
            return self.has_add_permission(request)
            
        # Check if user owns the organization or has appropriate role
        is_owner = OrganizationEmployeeHelper.is_user_owner(request.user, obj.organization)
        
        if is_owner:
            return True
            
        # Check if user has appropriate role in the organization
        has_role = OrganizationEmployee.objects.filter(
            user=request.user.username,
            organization=obj.organization,
            roles__title__in=['DIRECTOR', 'MANAGER', 'HR']
        ).exists()
        
        return has_role and super().has_change_permission(request, obj)
    
    def has_view_permission(self, request, obj = ...):
        return Organization.objects.filter(owner__user=request.user).exists()
    
    def has_delete_permission(self, request, obj=None):
        # Similar to change permission logic
        return self.has_change_permission(request, obj)