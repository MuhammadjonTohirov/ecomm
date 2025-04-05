from rest_framework import serializers
from crm.models.salary import EmployeeSalary, PaymentPeriod
from crm.models.attendance import EmployeeAttendance, AttendanceStatus
from crm.serializers.employee_serializers import OrganizationEmployeeSerializer


class EmployeeSalarySerializer(serializers.ModelSerializer):
    payment_period_display = serializers.CharField(source='get_payment_period_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    employee_details = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeSalary
        fields = [
            'id', 'employee', 'amount', 'currency', 'currency_display',
            'payment_period', 'payment_period_display', 'start_date', 
            'end_date', 'bonus_eligible', 'notes', 'created_date', 
            'updated_date', 'employee_details'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']
    
    def get_employee_details(self, obj):
        return {
            'username': obj.employee.user,
            'organization': obj.employee.organization.name
        }


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    employee_details = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeAttendance
        fields = [
            'id', 'employee', 'organization', 'date', 'check_in_time',
            'check_out_time', 'status', 'status_display', 'working_hours',
            'location', 'notes', 'created_date', 'updated_date',
            'employee_details'
        ]
        read_only_fields = ['id', 'working_hours', 'created_date', 'updated_date']
    
    def get_employee_details(self, obj):
        return {
            'username': obj.employee.user,
            'organization': obj.organization.name
        }


class AttendanceReportSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class SalaryCalculationSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class CheckInOutSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    location = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class SetSalarySerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.IntegerField()
    payment_period = serializers.ChoiceField(choices=PaymentPeriod.choices)
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False, allow_null=True)
    bonus_eligible = serializers.BooleanField(default=False)
    notes = serializers.CharField(required=False, allow_blank=True)