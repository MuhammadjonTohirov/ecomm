from django.contrib import admin
from django.utils.html import format_html
from crm.models.salary import EmployeeSalary, PaymentPeriod
from crm.models.attendance import EmployeeAttendance, AttendanceStatus
from crm.admin.base_admin_model import BaseAdminModel


@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(BaseAdminModel):
    list_display = ('employee', 'amount', 'currency_display', 'payment_period_display',
                    'start_date', 'end_date', 'is_active_display', 'bonus_eligible')
    list_filter = ('payment_period', 'currency', 'bonus_eligible', 'start_date')
    search_fields = ('employee__user', 'notes')
    date_hierarchy = 'start_date'
    
    fieldsets = [
        ('Salary Information', {
            'fields': ['employee', 'amount', 'currency', 'payment_period']
        }),
        ('Period', {
            'fields': ['start_date', 'end_date', 'bonus_eligible']
        }),
        ('Additional Information', {
            'fields': ['notes']
        }),
    ] + BaseAdminModel.fieldsets
    
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


@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(BaseAdminModel):
    list_display = ('employee', 'date', 'status_display', 'check_in_time_display',
                    'check_out_time_display', 'working_hours')
    list_filter = ('status', 'date', 'organization')
    search_fields = ('employee__user', 'notes', 'location')
    date_hierarchy = 'date'
    
    fieldsets = [
        ('Employee Information', {
            'fields': ['employee', 'organization']
        }),
        ('Attendance Details', {
            'fields': ['date', 'check_in_time', 'check_out_time', 'status', 'working_hours']
        }),
        ('Additional Information', {
            'fields': ['location', 'notes']
        }),
    ] + BaseAdminModel.fieldsets
    
    readonly_fields = ('working_hours',)
    
    def status_display(self, obj):
        status_colors = {
            AttendanceStatus.PRESENT: 'green',
            AttendanceStatus.LATE: 'orange',
            AttendanceStatus.HALF_DAY: 'blue',
            AttendanceStatus.ABSENT: 'red',
            AttendanceStatus.ON_LEAVE: 'purple'
        }
        color = status_colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
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
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter to only show attendance for employees in organizations the user has access to
        return qs.filter(organization__owner__user=request.user)