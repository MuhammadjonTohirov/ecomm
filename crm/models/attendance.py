from django.db import models
from django.utils import timezone
from crm.models.base_model import BaseModel
from crm.models.employee import OrganizationEmployee
from crm.models.organization import Organization


class AttendanceStatus(models.TextChoices):
    PRESENT = 'PRESENT', 'Present'
    LATE = 'LATE', 'Late'
    HALF_DAY = 'HALF_DAY', 'Half Day'
    ABSENT = 'ABSENT', 'Absent'
    ON_LEAVE = 'ON_LEAVE', 'On Leave'


class EmployeeAttendance(BaseModel):
    employee = models.ForeignKey(
        OrganizationEmployee, 
        on_delete=models.CASCADE, 
        related_name='attendances'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='employee_attendances'
    )
    date = models.DateField(
        verbose_name='Attendance Date',
        default=timezone.now
    )
    check_in_time = models.DateTimeField(
        verbose_name='Check-in Time',
        null=True, 
        blank=True
    )
    check_out_time = models.DateTimeField(
        verbose_name='Check-out Time',
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT,
        verbose_name='Attendance Status'
    )
    working_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        null=True, 
        blank=True,
        verbose_name='Working Hours'
    )
    location = models.CharField(
        max_length=255,
        null=True, 
        blank=True,
        verbose_name='Location'
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Notes'
    )

    class Meta:
        verbose_name = 'Employee Attendance'
        verbose_name_plural = 'Employee Attendances'
        ordering = ['-date', 'check_in_time']
        # Ensure one attendance record per employee per day
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.user} - {self.date} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        # Calculate working hours if both check-in and check-out times exist
        if self.check_in_time and self.check_out_time:
            # Calculate the timedelta and convert to decimal hours
            delta = self.check_out_time - self.check_in_time
            # Convert seconds to hours
            self.working_hours = round(delta.total_seconds() / 3600, 2)
            
            # Determine status based on organization's policy 
            # This is a simple example - you may need more complex logic
            if self.working_hours < 4:
                self.status = AttendanceStatus.HALF_DAY
            elif self.check_in_time.time() > timezone.datetime.strptime('09:30', '%H:%M').time():
                self.status = AttendanceStatus.LATE
            else:
                self.status = AttendanceStatus.PRESENT
                
        super().save(*args, **kwargs)