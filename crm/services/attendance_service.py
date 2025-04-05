from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from crm.models.employee import OrganizationEmployee
from crm.models.attendance import EmployeeAttendance, AttendanceStatus


class AttendanceService:
    """Service class to handle employee attendance operations"""
    
    @staticmethod
    def check_in(employee_id, location=None, notes=None):
        """
        Record employee check-in
        
        Args:
            employee_id: ID of the OrganizationEmployee
            location: Optional location information
            notes: Optional notes about check-in
            
        Returns:
            EmployeeAttendance: The created or updated attendance record
        """
        try:
            employee = OrganizationEmployee.objects.get(id=employee_id)
            current_time = timezone.now()
            today = current_time.date()
            
            # Check if an attendance record already exists for today
            attendance, created = EmployeeAttendance.objects.get_or_create(
                employee=employee,
                organization=employee.organization,
                date=today,
                defaults={
                    'check_in_time': current_time,
                    'status': AttendanceStatus.PRESENT,
                    'location': location,
                    'notes': notes,
                    'created_by': employee.user_object(),
                }
            )
            
            if not created:
                # If record exists but no check-in recorded yet
                if attendance.check_in_time is None:
                    attendance.check_in_time = current_time
                    attendance.location = location
                    if notes:
                        attendance.notes = notes
                    attendance.updated_by = employee.user_object()
                    attendance.save()
                else:
                    raise ValidationError("Employee has already checked in today")
            
            return attendance
        
        except OrganizationEmployee.DoesNotExist:
            raise ValidationError("Employee not found")
    
    @staticmethod
    def check_out(employee_id, location=None, notes=None):
        """
        Record employee check-out
        
        Args:
            employee_id: ID of the OrganizationEmployee
            location: Optional location information
            notes: Optional notes about check-out
            
        Returns:
            EmployeeAttendance: The updated attendance record
        """
        try:
            employee = OrganizationEmployee.objects.get(id=employee_id)
            current_time = timezone.now()
            today = current_time.date()
            
            try:
                # Find today's attendance record
                attendance = EmployeeAttendance.objects.get(
                    employee=employee,
                    date=today
                )
                
                # Validate check-out
                if attendance.check_in_time is None:
                    raise ValidationError("Cannot check out without checking in first")
                    
                if attendance.check_out_time is not None:
                    raise ValidationError("Employee has already checked out today")
                
                # Record check-out
                attendance.check_out_time = current_time
                if location:
                    attendance.location = location
                if notes:
                    attendance.notes = (attendance.notes or '') + f"\nCheck-out notes: {notes}"
                
                attendance.updated_by = employee.user_object()
                attendance.save()
                
                return attendance
                
            except EmployeeAttendance.DoesNotExist:
                raise ValidationError("No check-in record found for today")
        
        except OrganizationEmployee.DoesNotExist:
            raise ValidationError("Employee not found")
    
    @staticmethod
    def get_attendance_report(employee_id, start_date, end_date):
        """
        Generate attendance report for an employee within a date range
        
        Args:
            employee_id: ID of the OrganizationEmployee
            start_date: Start date for the report
            end_date: End date for the report
            
        Returns:
            dict: Report data including:
                - total_days: Total working days in period
                - present_days: Days employee was present
                - absent_days: Days employee was absent
                - late_days: Days employee was late
                - working_hours: Total working hours
                - attendance_records: List of attendance records
        """
        try:
            employee = OrganizationEmployee.objects.get(id=employee_id)
            
            # Get attendance records for the date range
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
            total_hours = sum(
                record.working_hours or 0 
                for record in records
            )
            
            # Create report
            report = {
                'employee': {
                    'id': employee.id,
                    'name': str(employee.user_object()),
                    'username': employee.user
                },
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'statistics': {
                    'total_days': (end_date - start_date).days + 1,
                    'present_days': present_count,
                    'late_days': late_count,
                    'half_days': half_day_count,
                    'absent_days': absent_count,
                    'total_working_hours': round(total_hours, 2)
                },
                'records': list(records.values(
                    'date', 'check_in_time', 'check_out_time', 
                    'status', 'working_hours', 'notes'
                ))
            }
            
            return report
            
        except OrganizationEmployee.DoesNotExist:
            raise ValidationError("Employee not found")