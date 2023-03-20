import random
from django import forms
from django.contrib import admin
from crm.admin.base_admin_model import BaseAdminModel
from crm.models.organization import Organization
from crm.models.customer import CustomerCard
from crm.models.models import Person

# customer admin


class RegularCustomerForm(forms.ModelForm):

    class Meta:
        model = CustomerCard
        fields = '__all__'

    user = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}), required=True
    )


@admin.register(CustomerCard)
class CustomerAdmin(BaseAdminModel):
    form = RegularCustomerForm
    list_display = ('user', 'card_number', 'by_organization', 'points', 'deposit', 'total_spent')
    fieldsets = [
        (None, {'fields': [
            'user', 'points', 'deposit', 'total_spent'
        ]})
    ] + BaseAdminModel.fieldsets

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.card_number = f'{obj.user.user.username}0{obj.user.user.id}'
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if db_field.name == "organization":
            # kwargs["queryset"] = Organization.objects.filter(belongs_to)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)