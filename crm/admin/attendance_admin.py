from crm.admin.base_admin_model import BaseAdminModel
from crm.models.attendance import AttendanceStatus, EmployeeAttendance


from django.contrib import admin
from django.utils.html import format_html


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

    class Meta:
        model = EmployeeAttendance
        fields = '__all__'
        exclude = ['created_date', 'updated_date']
        read_only_fields = ['created_date', 'updated_date']