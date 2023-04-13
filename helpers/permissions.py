from ast import List, Tuple
from django.contrib.auth.models import ContentType, Permission
from crm.models.employee_role import Role
from crm.models.organization import Organization
from crm.models.employee import EmployeeCareerLog, OrganizationEmployee

from crm.models.User import User
from helpers.enum import PermissionType
from sales.models import cart, news, order
from wms.models.Color import Color
from wms.models.Discount import Discount
from wms.models.product_core import ProductCore
from wms.models.stock_point import StockPoint3
from wms.models.stock_product import StockProduct
from wms.models.StockProductExtraFields import StockProductExtraFields
from wms.models.StockProductImage import StockProductImage


class ModelPermission:
    def __init__(self, user_id):
        self.user = User.objects.get(id=user_id)

    def add(self, model_name):
        content_type = ContentType.objects.get_for_model(model_name)
        permission = Permission.objects.get(
            codename='add_' + model_name._meta.model_name,
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)

    def view(self, model_name):
        content_type = ContentType.objects.get_for_model(model_name)
        permission = Permission.objects.get(
            codename='view_' + model_name._meta.model_name,
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)

    def edit(self, model_name):
        content_type = ContentType.objects.get_for_model(model_name)
        permission = Permission.objects.get(
            codename='change_' + model_name._meta.model_name,
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)

    def delete(self, model_name):
        content_type = ContentType.objects.get_for_model(model_name)
        permission = Permission.objects.get(
            codename='delete_' + model_name._meta.model_name,
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)

    def clear_all_permissions(self):
        self.user.user_permissions.clear()

    def get_permissions(self, model_name):
        content_type = ContentType.objects.get_for_model(model_name)
        change_permission = Permission.objects.get(
            codename='change_' + model_name._meta.model_name,
            content_type=content_type,
        )

        delete_permission = Permission.objects.get(
            codename='delete_' + model_name._meta.model_name,
            content_type=content_type,
        )

        view_permission = Permission.objects.get(
            codename='view_' + model_name._meta.model_name,
            content_type=content_type,
        )

        add_permission = Permission.objects.get(
            codename='view_' + model_name._meta.model_name,
            content_type=content_type,
        )
        
        return self.user.user_permissions.filter(id__in=[change_permission.id, delete_permission.id, view_permission.id, add_permission.id])

    def has_permission(self, model_name, permission):
        content_type = ContentType.objects.get_for_model(model_name)
        permission = Permission.objects.get(
            codename=permission + '_' + model_name._meta.model_name,
            content_type=content_type,
        )
        return self.get_permissions(model_name).contains(permission)

    def has_change_permission(self, model_name):
        return self.has_permission(model_name, 'change')

    def has_create_permission(self, model_name):
        return self.has_permission(model_name, 'add')

    def has_delete_permission(self, model_name):
        return self.has_permission(model_name, 'delete')

    def has_edit_permission(self, model_name):
        return self.has_change_permission(model_name) or self.has_create_permission(model_name) or self.has_delete_permission(model_name)

    def has_view_permission(self, model_name):
        return self.has_permission(model_name, 'view')
    
    def has_permission_on(self, model_name, type: PermissionType) -> bool:
        self.has_permission(model_name, type.title)
        
    def add_permission_on(self, model_name, type: PermissionType):
        content_type = ContentType.objects.get_for_model(model_name)
        permission = Permission.objects.get(
            codename=type.title + '_' + model_name._meta.model_name,
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        
    def add_permissions_on(self, model_name, types: tuple):
        for type in types:
            self.add_permission_on(model_name, type)
        
    def delete_permission_on(self, model_name, type: PermissionType):
        content_type = ContentType.objects.get_for_model(model_name)
        permission = Permission.objects.get(
            codename=type.title + '_' + model_name._meta.model_name,
            content_type=content_type,
        )
        self.user.user_permissions.remove(permission)
    
    def delete_permissions_on(self, model_name, types: tuple):
        for type in types:
            self.delete_permission_on(model_name, type)


class PermissionManager:
    def defaultPermissionForBusinessUser(self, user_id):
        modelPermission = ModelPermission(user_id)
        
        def crudFor(model):
            modelPermission.add(model)
            modelPermission.view(model)
            modelPermission.edit(model)
            modelPermission.delete(model)

        crudFor(Organization)
        crudFor(OrganizationEmployee)

        modelPermission.view(ProductCore)

        crudFor(StockProduct)
        crudFor(StockPoint3)
        crudFor(StockProductExtraFields)
        crudFor(StockProductImage)
        crudFor(Discount)
        crudFor(Color)
        crudFor(cart.Cart)
        crudFor(news.News)
        crudFor(order.Order)
        crudFor(Role)
        crudFor(EmployeeCareerLog)
    
    def defaultPermissionForSimpleUser(self, user_id):
        modelPermission = ModelPermission(user_id)
        modelPermission.clear_all_permissions()
    
    # def hrPermission(self, user_id):
    #     modelPermission = ModelPermission(user_id)
    #     modelPermission.clear_all_permissions()
    #     modelPermission.add_permissions_on(OrganizationEmployee, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
    #     modelPermission.add_permissions_on(Organization, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
    #     modelPermission.add_permissions_on(Role, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
    #     modelPermission.add_permissions_on(EmployeeCareerLog, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
        
    # def removeHrPermission(self, user_id):
    #     modelPermission = ModelPermission(user_id)
    #     modelPermission.delete_permissions_on(OrganizationEmployee, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
    #     modelPermission.delete_permissions_on(Organization, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
    #     modelPermission.delete_permissions_on(Role, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
    #     modelPermission.delete_permissions_on(EmployeeCareerLog, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD))
        
    # def managerPermission(self, user_id):
    #     modelPermission = ModelPermission(user_id)
    #     modelPermission.clear_all_permissions()
    #     modelPermission.add_permissions_on(OrganizationEmployee, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
    #     modelPermission.add_permissions_on(Organization, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
    #     modelPermission.add_permissions_on(Role, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
    #     modelPermission.add_permissions_on(EmployeeCareerLog, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
        
    # def removeManagerPermission(self, user_id):
    #     modelPermission = ModelPermission(user_id)
    #     modelPermission.delete_permissions_on(OrganizationEmployee, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
    #     modelPermission.delete_permissions_on(Organization, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
    #     modelPermission.delete_permissions_on(Role, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
    #     modelPermission.delete_permissions_on(EmployeeCareerLog, (PermissionType.VIEW, PermissionType.CHANGE, PermissionType.ADD, PermissionType.DELETE))
