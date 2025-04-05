from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from crm.models.employee import OrganizationEmployee
from crm.models.salary import EmployeeSalary, PaymentPeriod
from crm.models.attendance import EmployeeAttendance, AttendanceStatus
from crm.services.attendance_service import AttendanceService
from crm.services.salary_service import SalaryService
from helpers.responses import AppResponse
from crm.serializers.serializers import OrganizationSmallSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in(request):
    """
    API endpoint for employee check-in
    """
    try:
        employee_id = request.data.get('employee_id')
        location = request.data.get('location')
        notes = request.data.get('notes')
        
        if not employee_id:
            return Response(AppResponse('Employee ID is required').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        attendance = AttendanceService.check_in(
            employee_id=employee_id,
            location=location,
            notes=notes
        )
        
        # Return response
        response_data = {
            'id': attendance.id,
            'employee': attendance.employee.user,
            'date': attendance.date,
            'check_in_time': attendance.check_in_time,
            'status': attendance.get_status_display()
        }
        
        return Response(AppResponse(response_data).body(), status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response(AppResponse(str(e)).error_body(), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(AppResponse(f"Error during check-in: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out(request):
    """
    API endpoint for employee check-out
    """
    try:
        employee_id = request.data.get('employee_id')
        location = request.data.get('location')
        notes = request.data.get('notes')
        
        if not employee_id:
            return Response(AppResponse('Employee ID is required').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        attendance = AttendanceService.check_out(
            employee_id=employee_id,
            location=location,
            notes=notes
        )
        
        # Return response
        response_data = {
            'id': attendance.id,
            'employee': attendance.employee.user,
            'date': attendance.date,
            'check_in_time': attendance.check_in_time,
            'check_out_time': attendance.check_out_time,
            'working_hours': attendance.working_hours,
            'status': attendance.get_status_display()
        }
        
        return Response(AppResponse(response_data).body(), status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response(AppResponse(str(e)).error_body(), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(AppResponse(f"Error during check-out: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance_report(request):
    """
    API endpoint to get attendance report for an employee
    """
    try:
        employee_id = request.GET.get('employee_id')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        if not employee_id:
            return Response(AppResponse('Employee ID is required').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        if not start_date_str or not end_date_str:
            return Response(AppResponse('Start date and end date are required').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(AppResponse('Invalid date format. Use YYYY-MM-DD').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        report = AttendanceService.get_attendance_report(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return Response(AppResponse(report).body(), status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response(AppResponse(str(e)).error_body(), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(AppResponse(f"Error generating report: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_employee_salary(request):
    """
    API endpoint to set employee salary
    """
    try:
        employee_id = request.data.get('employee_id')
        amount = request.data.get('amount')
        currency = request.data.get('currency')
        payment_period = request.data.get('payment_period')
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')
        bonus_eligible = request.data.get('bonus_eligible', False)
        notes = request.data.get('notes')
        
        # Validate required fields
        if not all([employee_id, amount, currency, payment_period, start_date_str]):
            return Response(AppResponse('Missing required fields').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError:
            return Response(AppResponse('Invalid date format. Use YYYY-MM-DD').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Set salary
        salary = SalaryService.set_salary(
            employee_id=employee_id,
            amount=amount,
            currency=currency,
            payment_period=payment_period,
            start_date=start_date,
            end_date=end_date,
            bonus_eligible=bonus_eligible,
            notes=notes,
            created_by=request.user
        )
        
        # Return response
        response_data = {
            'id': salary.id,
            'employee': salary.employee.user,
            'amount': float(salary.amount),
            'currency': salary.get_currency_display(),
            'payment_period': salary.get_payment_period_display(),
            'start_date': salary.start_date,
            'end_date': salary.end_date
        }
        
        return Response(AppResponse(response_data).body(), status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response(AppResponse(str(e)).error_body(), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(AppResponse(f"Error setting salary: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_salary(request):
    """
    API endpoint to get current salary for an employee
    """
    try:
        employee_id = request.GET.get('employee_id')
        
        if not employee_id:
            return Response(AppResponse('Employee ID is required').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        salary = SalaryService.get_current_salary(employee_id=employee_id)
        
        if not salary:
            return Response(AppResponse('No active salary found for employee').error_body(), 
                           status=status.HTTP_404_NOT_FOUND)
        
        # Return response
        response_data = {
            'id': salary.id,
            'employee': salary.employee.user,
            'amount': float(salary.amount),
            'currency': salary.get_currency_display(),
            'payment_period': salary.get_payment_period_display(),
            'start_date': salary.start_date,
            'end_date': salary.end_date,
            'bonus_eligible': salary.bonus_eligible,
            'notes': salary.notes
        }
        
        return Response(AppResponse(response_data).body(), status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response(AppResponse(str(e)).error_body(), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(AppResponse(f"Error retrieving salary: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calculate_salary_period(request):
    """
    API endpoint to calculate salary for a specific period
    """
    try:
        employee_id = request.GET.get('employee_id')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        if not employee_id:
            return Response(AppResponse('Employee ID is required').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        if not start_date_str or not end_date_str:
            return Response(AppResponse('Start date and end date are required').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(AppResponse('Invalid date format. Use YYYY-MM-DD').error_body(), 
                           status=status.HTTP_400_BAD_REQUEST)
        
        calculation = SalaryService.calculate_salary_for_period(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return Response(AppResponse(calculation).body(), status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response(AppResponse(str(e)).error_body(), status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(AppResponse(f"Error calculating salary: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_attendance(request):
    """
    API endpoint to get attendance report for an entire organization
    """
    try:
        organization_id = request.GET.get('organization_id')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        department = request.GET.get('department')  # Optional department filter
        
        if not organization_id:
            return Response(AppResponse('Organization ID is required').error_body(), 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if not start_date_str or not end_date_str:
            return Response(AppResponse('Start date and end date are required').error_body(), 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Check permission
        if not request.user.is_superuser:
            employee = OrganizationEmployee.objects.filter(
                user=request.user.username,
                organization_id=organization_id
            ).first()
            
            if not employee or not any(role.title in ['DIRECTOR', 'MANAGER', 'HR'] for role in employee.roles.all()):
                return Response(AppResponse('You do not have permission to view organization attendance').error_body(), 
                              status=status.HTTP_403_FORBIDDEN)
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(AppResponse('Invalid date format. Use YYYY-MM-DD').error_body(), 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Get all employees in the organization
        employees = OrganizationEmployee.objects.filter(organization_id=organization_id)
        
        # Get attendance for all employees
        attendance_data = []
        for employee in employees:
            # Get attendance records
            records = EmployeeAttendance.objects.filter(
                employee=employee,
                date__range=(start_date, end_date)
            ).order_by('date')
            
            # Calculate statistics
            present_count = records.filter(status=AttendanceStatus.PRESENT).count()
            late_count = records.filter(status=AttendanceStatus.LATE).count()
            half_day_count = records.filter(status=AttendanceStatus.HALF_DAY).count()
            absent_count = records.filter(status=AttendanceStatus.ABSENT).count()
            
            # Calculate total working hours
            total_hours = sum(record.working_hours or 0 for record in records)
            
            attendance_data.append({
                'employee': {
                    'id': employee.id,
                    'username': employee.user,
                    'name': str(employee.user_object()) if hasattr(employee, 'user_object') else employee.user
                },
                'statistics': {
                    'present_days': present_count,
                    'late_days': late_count,
                    'half_days': half_day_count,
                    'absent_days': absent_count,
                    'total_working_hours': round(float(total_hours), 2) if total_hours else 0
                },
                'last_attendance': {
                    'date': records.last().date if records.exists() else None,
                    'status': records.last().get_status_display() if records.exists() else None
                }
            })
        
        return Response(AppResponse({
            'organization_id': organization_id,
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'employee_count': len(attendance_data),
            'employees': attendance_data
        }).body(), status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(AppResponse(f"Error retrieving organization attendance: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_salary_summary(request):
    """
    API endpoint to get salary summary for an entire organization
    """
    try:
        organization_id = request.GET.get('organization_id')
        
        if not organization_id:
            return Response(AppResponse('Organization ID is required').error_body(), 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Check permission
        if not request.user.is_superuser:
            employee = OrganizationEmployee.objects.filter(
                user=request.user.username,
                organization_id=organization_id
            ).first()
            
            if not employee or not any(role.title in ['DIRECTOR', 'MANAGER', 'ACCOUNTANT'] for role in employee.roles.all()):
                return Response(AppResponse('You do not have permission to view organization salary data').error_body(), 
                              status=status.HTTP_403_FORBIDDEN)
        
        # Get all employees in the organization
        employees = OrganizationEmployee.objects.filter(organization_id=organization_id)
        
        # Get salary data for all employees
        salary_data = []
        total_monthly_sum = 0
        total_monthly_dollar = 0
        total_monthly_euro = 0
        
        for employee in employees:
            # Get current salary
            current_salary = SalaryService.get_current_salary(employee.id)
            
            if current_salary:
                employee_data = {
                    'employee': {
                        'id': employee.id,
                        'username': employee.user,
                        'name': str(employee.user_object()) if hasattr(employee, 'user_object') else employee.user
                    },
                    'salary': {
                        'id': current_salary.id,
                        'amount': float(current_salary.amount),
                        'currency': current_salary.get_currency_display(),
                        'payment_period': current_salary.get_payment_period_display(),
                        'start_date': current_salary.start_date,
                        'bonus_eligible': current_salary.bonus_eligible
                    }
                }
                
                salary_data.append(employee_data)
                
                # Add to totals (for monthly equivalent)
                if current_salary.payment_period == PaymentPeriod.MONTHLY:
                    monthly_amount = float(current_salary.amount)
                elif current_salary.payment_period == PaymentPeriod.WEEKLY:
                    monthly_amount = float(current_salary.amount) * 4.33  # Avg weeks in month
                elif current_salary.payment_period == PaymentPeriod.DAILY:
                    monthly_amount = float(current_salary.amount) * 22  # Avg working days in month
                
                if current_salary.currency == 1:  # Sum
                    total_monthly_sum += monthly_amount
                elif current_salary.currency == 2:  # Dollar
                    total_monthly_dollar += monthly_amount
                elif current_salary.currency == 3:  # Euro
                    total_monthly_euro += monthly_amount
        
        return Response(AppResponse({
            'organization_id': organization_id,
            'employee_count': len(salary_data),
            'monthly_totals': {
                'sum': round(total_monthly_sum, 2),
                'dollar': round(total_monthly_dollar, 2),
                'euro': round(total_monthly_euro, 2)
            },
            'employees': salary_data
        }).body(), status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(AppResponse(f"Error retrieving organization salary data: {str(e)}").error_body(), 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)