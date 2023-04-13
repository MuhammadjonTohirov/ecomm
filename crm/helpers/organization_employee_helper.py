from django.db.models import Q
from datetime import datetime

from django.http import HttpRequest
from crm.models.employee_role import Role
from crm.models.models import Person
from crm.models.organization import Organization
from crm.models.employee import OrganizationEmployee
from crm.models.User import User


class OrganizationEmployeeHelper:
    @staticmethod
    def works_in_organization(user: User, organization: Organization):
        return OrganizationEmployee.objects.filter(user=user.username, organization=organization).exists()
    
    @staticmethod
    def is_user_owner(user: User, organization: Organization):
        return organization.owner.user == user

    @staticmethod
    def get_active_organizations(user: User) -> list:
        """_summary_
        Returns list of organizations where user currenlty working.
        """
        orgs = OrganizationEmployee.objects\
            .filter(user=user.username).values('organization').distinct()
        person = Person.objects.filter(user=user).first()
        return Organization.objects.filter(Q(id__in=orgs) | Q(owner=person))

    @staticmethod
    def get_all_organizations(user: User) -> list:
        """_summary_
        Returns list of organizations where user currenlty working.
        """
        person = Person.objects.filter(user=user).first()
        orgs = OrganizationEmployee.objects.filter(
            user=user.username).values('organization').distinct()
        return Organization.objects.filter(Q(id__in=orgs) | Q(owner=person))

    @staticmethod
    def create_employee(username: str, request: HttpRequest, organization, role: Role):
        employee = OrganizationEmployee.objects.get(
            user=username, organization=organization)
        if employee is not None:
            if not employee.roles.contains(role):
                employee.roles.add(role)
                employee.roles.update_date = datetime.now()
                employee.save()
            return

        employee = OrganizationEmployee.objects.update_or_create(
            user=username, organization=organization, created_by=request.user)[0]
        
        # EmployeeCareerLog.objects.create(
        #     employee.
