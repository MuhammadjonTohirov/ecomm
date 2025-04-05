from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from crm.models.employee import OrganizationEmployee
from crm.models.attendance import EmployeeAttendance


@login_required
def attendance_tracking(request):
    """
    View for employee attendance tracking page
    """
    # Get the employee record for the current user
    try:
        employee = OrganizationEmployee.objects.filter(user=request.user.username).first()
        
        if not employee:
            # User is not registered as an employee
            return render(request, 'eui/errors/404.html', {
                'message': 'You are not registered as an employee in any organization.'
            })
        
        context = {
            'active_module': 'crm',
            'active_submenu': 'attendance',
            'employee': employee
        }
        
        return render(request, 'eui/crm/attendance_tracking.html', context)
    
    except Exception as e:
        # Log the error
        print(f"Error in attendance_tracking view: {str(e)}")
        return render(request, 'eui/errors/500.html', {
            'message': 'An error occurred while loading the attendance tracking page.'
        })


@login_required
def salary_detail(request):
    """
    View for employee salary details page
    """
    # Get the employee record for the current user
    try:
        employee = OrganizationEmployee.objects.filter(user=request.user.username).first()
        
        if not employee:
            # User is not registered as an employee
            return render(request, 'eui/errors/404.html', {
                'message': 'You are not registered as an employee in any organization.'
            })
        
        context = {
            'active_module': 'crm',
            'active_submenu': 'salary',
            'employee': employee
        }
        
        return render(request, 'eui/crm/salary_detail.html', context)
    
    except Exception as e:
        # Log the error
        print(f"Error in salary_detail view: {str(e)}")
        return render(request, 'eui/errors/500.html', {
            'message': 'An error occurred while loading the salary details page.'
        })


@login_required
def admin_attendance_report(request, organization_id=None):
    """
    View for organization admin to see attendance reports
    """
    # Check if user is authorized to view this organization's attendance
    try:
        if not organization_id:
            # Redirect to the first organization the user has access to
            organizations = OrganizationEmployee.get_active_organizations(request.user)
            if organizations.exists():
                organization_id = organizations.first().id
            else:
                return render(request, 'eui/errors/404.html', {
                    'message': 'You do not have access to any organizations.'
                })
        
        # Check if the user has permission to view this organization
        if not request.user.is_superuser:
            employee = OrganizationEmployee.objects.filter(
                user=request.user.username,
                organization_id=organization_id
            ).first()
            
            if not employee:
                return render(request, 'eui/errors/403.html', {
                    'message': 'You do not have permission to view this organization.'
                })
        
        context = {
            'active_module': 'crm',
            'active_submenu': 'attendance_admin',
            'organization_id': organization_id
        }
        
        return render(request, 'eui/crm/admin_attendance_report.html', context)
    
    except Exception as e:
        # Log the error
        print(f"Error in admin_attendance_report view: {str(e)}")
        return render(request, 'eui/errors/500.html', {
            'message': 'An error occurred while loading the attendance report page.'
        })


@login_required
def admin_salary_management(request, organization_id=None):
    """
    View for organization admin to manage employee salaries
    """
    # Check if user is authorized to view this organization's salary data
    try:
        if not organization_id:
            # Redirect to the first organization the user has access to
            organizations = OrganizationEmployee.get_active_organizations(request.user)
            if organizations.exists():
                organization_id = organizations.first().id
            else:
                return render(request, 'eui/errors/404.html', {
                    'message': 'You do not have access to any organizations.'
                })
        
        # Check if the user has permission to view this organization
        if not request.user.is_superuser:
            employee = OrganizationEmployee.objects.filter(
                user=request.user.username,
                organization_id=organization_id
            ).first()
            
            if not employee:
                return render(request, 'eui/errors/403.html', {
                    'message': 'You do not have permission to view this organization.'
                })
        
        context = {
            'active_module': 'crm',
            'active_submenu': 'salary_admin',
            'organization_id': organization_id
        }
        
        return render(request, 'eui/crm/admin_salary_management.html', context)
    
    except Exception as e:
        # Log the error
        print(f"Error in admin_salary_management view: {str(e)}")
        return render(request, 'eui/errors/500.html', {
            'message': 'An error occurred while loading the salary management page.'
        })