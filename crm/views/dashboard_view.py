from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from crm.models.organization import Organization
from crm.models.employee import OrganizationEmployee
from crm.helpers.organization_employee_helper import OrganizationEmployeeHelper
from crm.serializers.serializers import OrganizationSmallSerializer, PersonSerializer
from helpers.responses import AppResponse
from crm.serializers.employee_serializers import OrganizationEmployeeSerializer


def crm_dashboard(request):
    """
    Render the CRM dashboard template
    """
    if request.user is None or not request.user.is_authenticated:
        return render(request, 'eui/others/404.html', {'message': 'User not authenticated'})
    
    # Get top 5 organizations by created_date (most recent first)
    organizations = OrganizationEmployeeHelper.get_active_organizations(request.user).order_by('-created_date')[:5]
    organization_count = organizations.count()
    
    employee_count = 0
    
    for org in organizations:
        employee_count += OrganizationEmployee.objects.filter(organization=org).count()
    
    context = {
        'active_module': 'crm',
        'organization_count': organization_count,
        'employee_count': employee_count,
        'organizations': organizations  # Pass organizations to template
    }
    
    return render(request, 'eui/crm/dashboard.html', context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organizations(request):
    """
    API endpoint to get top 5 organizations for the current user
    """
    organizations = OrganizationEmployeeHelper.get_active_organizations(request.user).order_by('-created_date')[:5]
    serializer = OrganizationSmallSerializer(organizations, many=True)
    return Response(AppResponse(serializer.data).body())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employees(request):
    """
    API endpoint to get employees for a specific organization
    """
    organization_id = request.GET.get('organization_id', None)
    
    if not organization_id:
        return Response(AppResponse('Organization ID is required').error_body())
    
    employees = OrganizationEmployee.objects.filter(organization_id=organization_id)
    serializer = OrganizationEmployeeSerializer(employees, many=True)
    return Response(AppResponse(serializer.data).body())

def employee_detail(request, employee_id):
    """
    View employee details
    """
    try:
        employee = OrganizationEmployee.objects.get(id=employee_id)
        user = None
        try:
            from crm.models.User import User
            user = User.objects.get(username=employee.user)
        except User.DoesNotExist:
            pass
            
        context = {
            'active_module': 'crm',
            'employee': employee,
            'user': user,
            'roles': employee.roles.all()
        }
        return render(request, 'eui/crm/employee_detail.html', context)
    except OrganizationEmployee.DoesNotExist:
        return render(request, 'eui/errors/404.html', {'message': 'Employee not found'})