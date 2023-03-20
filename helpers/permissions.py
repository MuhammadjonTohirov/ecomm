from django.contrib.auth.models import ContentType, Permission
from crm.models.organization import Organization
from crm.models.OrganizationEmployee import OrganizationEmployee

from crm.models.User import User
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


class PermissionManager:
    def defaultPermissionForBusinessUser(self, user_id):
        modelPermission = ModelPermission(user_id)

        def crudFor(model):
            modelPermission.add(model)
            modelPermission.view(model)
            modelPermission.edit(model)

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

    def defaultPermissionForSimpleUser(self, user_id):
        modelPermission = ModelPermission(user_id)
        modelPermission.clear_all_permissions()
