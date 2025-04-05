from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
import calendar
from datetime import datetime, timedelta

from crm.models.employee import OrganizationEmployee
from crm.models.salary import EmployeeSalary, PaymentPeriod
from crm.models.attendance import EmployeeAttendance, AttendanceStatus


class SalaryService:
    """Service class to handle employee salary operations"""
    
    @staticmethod
    def set_salary(employee_id, amount, currency, payment_period, 
                  start_date, end_date=None, bonus_eligible=False, notes=None, created_by=None):
        """
        Set or update employee salary
        
        Args:
            employee_id: ID of the OrganizationEmployee
            amount: Salary amount
            currency: Currency type (from Currency enum)
            payment_period: PaymentPeriod (DAILY, WEEKLY, MONTHLY)
            start_date: When this salary becomes effective
            end_date: Optional end date for this salary rate
            bonus_eligible: Whether employee is eligible for bonuses
            notes: Optional notes about the salary
            created_by: User who created this record
            
        Returns:
            EmployeeSalary: The created salary record
        """
        try:
            employee = OrganizationEmployee.objects.get(id=employee_id)
            
            # If there's an existing active salary, end it as of yesterday
            with transaction.atomic():
                active_salaries = EmployeeSalary.objects.filter(
                    employee=employee,
                    start_date__lte=start_date,
                    end_date__isnull=True
                )
                
                for salary in active_salaries:
                    # Set end date to the day before the new salary starts
                    salary.end_date = start_date - timedelta(days=1)
                    salary.updated_by = created_by
                    salary.save()
                
                # Create new salary record
                new_salary = EmployeeSalary.objects.create(
                    employee=employee,
                    amount=amount,
                    currency=currency,
                    payment_period=payment_period,
                    start_date=start_date,
                    end_date=end_date,
                    bonus_eligible=bonus_eligible,
                    notes=notes,
                    created_by=created_by
                )
                
                return new_salary
                
        except OrganizationEmployee.DoesNotExist:
            raise ValidationError("Employee not found")
    
    @staticmethod
    def get_current_salary(employee_id):
        """
        Get employee's current salary
        
        Args:
            employee_id: ID of the OrganizationEmployee
            
        Returns:
            EmployeeSalary: The active salary record or None
        """
        try:
            employee = OrganizationEmployee.objects.get(id=employee_id)
            today = timezone.now().date()
            
            # Find salary record that's active today
            current_salary = EmployeeSalary.objects.filter(
                employee=employee,
                start_date__lte=today,
                end_date__isnull=True
            ).first()
            
            if not current_salary:
                # Also check if there's a record with a future end date
                current_salary = EmployeeSalary.objects.filter(
                    employee=employee,
                    start_date__lte=today,
                    end_date__gte=today
                ).first()
            
            return current_salary
            
        except OrganizationEmployee.DoesNotExist:
            raise ValidationError("Employee not found")
    
    @staticmethod
    def calculate_salary_for_period(employee_id, start_date, end_date):
        """
        Calculate salary for a specific period, taking into account attendance
        
        Args:
            employee_id: ID of the OrganizationEmployee
            start_date: Start date for the calculation
            end_date: End date for the calculation
            
        Returns:
            dict: Salary calculation details
        """
        try:
            employee = OrganizationEmployee.objects.get(id=employee_id)
            
            # Get current salary
            salary = SalaryService.get_current_salary(employee_id)
            if not salary:
                raise ValidationError("No active salary found for employee")
            
            # Get attendance records for the period
            attendance_records = EmployeeAttendance.objects.filter(
                employee=employee,
                date__range=(start_date, end_date)
            )
            
            # Count working days in the period
            working_days = (end_date - start_date).days + 1
            
            # Count present, half-day, and absent days
            present_days = attendance_records.filter(
                status__in=[AttendanceStatus.PRESENT, AttendanceStatus.LATE]
            ).count()
            
            half_days = attendance_records.filter(
                status=AttendanceStatus.HALF_DAY
            ).count()
            
            absent_days = attendance_records.filter(
                status=AttendanceStatus.ABSENT
            ).count()
            
            # Calculate base salary for the period
            base_amount = salary.amount
            
            # Adjust based on payment period
            if salary.payment_period == PaymentPeriod.MONTHLY:
                # Calculate days in the month for pro-rating
                _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
                daily_rate = base_amount / Decimal(days_in_month)
                calculated_amount = daily_rate * (present_days + (half_days * Decimal('0.5')))
                
            elif salary.payment_period == PaymentPeriod.WEEKLY:
                daily_rate = base_amount / Decimal('7')
                calculated_amount = daily_rate * (present_days + (half_days * Decimal('0.5')))
                
            elif salary.payment_period == PaymentPeriod.DAILY:
                calculated_amount = base_amount * (present_days + (half_days * Decimal('0.5')))
            
            # Create calculation result
            result = {
                'employee': {
                    'id': employee.id,
                    'name': str(employee.user_object()),
                    'username': employee.user
                },
                'period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'working_days': working_days
                },
                'attendance': {
                    'present_days': present_days,
                    'half_days': half_days,
                    'absent_days': absent_days
                },
                'salary': {
                    'base_amount': float(base_amount),
                    'currency': salary.get_currency_display(),
                    'payment_period': salary.get_payment_period_display(),
                    'calculated_amount': float(calculated_amount)
                }
            }
            
            return result
            
        except OrganizationEmployee.DoesNotExist:
            raise ValidationError("Employee not found")