from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from crm.models.organization import Organization
from crm.models.client import Client
from crm.models.employee import OrganizationEmployee
from crm.helpers.organization_employee_helper import OrganizationEmployeeHelper
from crm.serializers.serializers import OrganizationSmallSerializer, PersonSerializer
from helpers.responses import AppResponse
from crm.serializers.employee_serializers import OrganizationEmployeeSerializer


def crm_dashboard(request):
    """
    Render the CRM dashboard template
    """
    organizations = OrganizationEmployeeHelper.get_active_organizations(request.user)
    organization_count = organizations.count()
    
    # Get clients count across all organizations
    client_count = 0
    employee_count = 0
    
    for org in organizations:
        client_count += Client.objects.filter(organization=org).count()
        employee_count += OrganizationEmployee.objects.filter(organization=org).count()
    
    context = {
        'active_module': 'crm',
        'organization_count': organization_count,
        'client_count': client_count,
        'employee_count': employee_count
    }
    
    return render(request, 'eui/crm/dashboard.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organizations(request):
    """
    API endpoint to get organizations for the current user
    """
    organizations = OrganizationEmployeeHelper.get_active_organizations(request.user)
    serializer = OrganizationSmallSerializer(organizations, many=True)
    return Response(AppResponse(serializer.data).body())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_clients(request):
    """
    API endpoint to get clients for a specific organization
    """
    organization_id = request.GET.get('organization_id', None)
    
    if not organization_id:
        return Response(AppResponse('Organization ID is required').error_body())
    
    clients = Client.objects.filter(organization_id=organization_id)
    persons = [client.user for client in clients]
    
    serializer = PersonSerializer(persons, many=True, context={'organization_id': organization_id})
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


def client_detail(request, client_id):
    """
    View client details
    """
    try:
        client = Client.objects.get(id=client_id)
        context = {
            'active_module': 'crm',
            'client': client,
            'person': client.user
        }
        return render(request, 'eui/crm/client_detail.html', context)
    except Client.DoesNotExist:
        return render(request, 'eui/errors/404.html', {'message': 'Client not found'})


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