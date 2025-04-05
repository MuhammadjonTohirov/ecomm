from django.db import models
from crm.models.base_model import BaseModel
from crm.models.employee import OrganizationEmployee
from helpers.enum import Currency


class PaymentPeriod(models.TextChoices):
    DAILY = 'DAILY', 'Daily'
    WEEKLY = 'WEEKLY', 'Weekly'
    MONTHLY = 'MONTHLY', 'Monthly'


class EmployeeSalary(BaseModel):
    employee = models.ForeignKey(
        OrganizationEmployee, 
        on_delete=models.CASCADE, 
        related_name='salaries'
    )
    amount = models.DecimalField(
        verbose_name='Salary Amount',
        max_digits=12, 
        decimal_places=2
    )
    currency = models.SmallIntegerField(
        choices=Currency.__list__, 
        default=1,  # Default to Sum from your Currency enum
        verbose_name='Currency'
    )
    payment_period = models.CharField(
        max_length=10,
        choices=PaymentPeriod.choices,
        default=PaymentPeriod.MONTHLY,
        verbose_name='Payment Period'
    )
    start_date = models.DateField(
        verbose_name='Start Date',
        help_text='Date when this salary rate becomes effective'
    )
    end_date = models.DateField(
        verbose_name='End Date', 
        null=True, 
        blank=True,
        help_text='Date when this salary rate ends (leave blank if currently active)'
    )
    bonus_eligible = models.BooleanField(
        default=False, 
        verbose_name='Eligible for Bonus'
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Notes'
    )

    class Meta:
        verbose_name = 'Employee Salary'
        verbose_name_plural = 'Employee Salaries'
        ordering = ['-start_date', 'employee']

    def __str__(self):
        currency_display = dict(Currency.__list__).get(self.currency, 'Unknown')
        return f"{self.employee.user} - {self.amount} {currency_display} ({self.get_payment_period_display()})"

    def is_active(self):
        """Check if this salary entry is currently active"""
        from django.utils import timezone
        today = timezone.now().date()
        return (self.start_date <= today and 
                (self.end_date is None or self.end_date >= today))