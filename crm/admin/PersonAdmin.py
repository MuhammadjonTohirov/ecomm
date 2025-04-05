from django import forms
from crm.admin.base_admin_model import BaseAdminModel
from crm.models.User import User
from crm.models.client import Client
from crm.models.models import Person
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.auth.models import Permission

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        print(self.user)

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean(self):
        return super().clean()


@admin.register(Person)
class PersonAdmin(BaseAdminModel):
    form = PersonForm
    list_display = ('user', 'created_date', 'updated_date')
    fieldsets = [
        ('Person', {'fields': ['user', 'is_business', 'avatar', 'phone_number', 'email', 'address']})] + BaseAdminModel.fieldsets

    def id(self):
        return self.user.id

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if self.id == request.user.id:
            return True

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(user=request.user)

@admin.register(Client)
class ClientAdmin(BaseAdminModel):
    list_display = ('user', 'created_date', 'updated_date')
    fieldsets = [
        ('Client', {'fields': ['user', 'organization', 'cashback', 'balance']})] + BaseAdminModel.fieldsets

    def id(self):
        return self.user.id

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if self.id == request.user.id:
            return True

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(user=request.user)